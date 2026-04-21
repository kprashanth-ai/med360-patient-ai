import asyncio
import argparse
import sys
import itertools
from pathlib import Path
from colorama import init, Fore, Style

from app.services.chat_service import attach_report as chat_attach_report
from app.services.chat_service import send_message, start_chat
from app.services.llm import build_patient_info, get_recommendation
from app.services.report_service import interpret_report
from app.tracker import get_session_totals

init(autoreset=True)

URGENCY_COLOR = {
    "low":       Fore.GREEN,
    "moderate":  Fore.YELLOW,
    "high":      Fore.RED,
    "emergency": Fore.RED + Style.BRIGHT,
}

STEP_COLOR = {
    "monitor":      Fore.GREEN,
    "teleconsult":  Fore.CYAN,
    "home_visit":   Fore.CYAN,
    "specialist":   Fore.YELLOW,
    "emergency":    Fore.RED + Style.BRIGHT,
}


def header(text):
    width = 48
    print()
    print(Style.BRIGHT + "┌" + "─" * (width - 2) + "┐")
    print(Style.BRIGHT + "│" + f"  {text}".ljust(width - 2) + "│")
    print(Style.BRIGHT + "└" + "─" * (width - 2) + "┘")


def section(title):
    print()
    print(Style.BRIGHT + Fore.CYAN + f"  {title}")
    print(Fore.CYAN + "  " + "─" * 44)


def row(label, value, value_color=""):
    label_str = f"  {label:<22}"
    print(Style.BRIGHT + label_str + Style.RESET_ALL + value_color + value + Style.RESET_ALL)


async def animate_analyzing():
    """Runs a spinner until cancelled."""
    frames = ["   Analyzing   ", "   Analyzing.  ", "   Analyzing.. ", "   Analyzing..."]
    for frame in itertools.cycle(frames):
        sys.stdout.write(f"\r{Fore.CYAN}{Style.BRIGHT}{frame}{Style.RESET_ALL}")
        sys.stdout.flush()
        await asyncio.sleep(0.4)


def _input_int(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            print(Fore.RED + f"    Must be between {min_val} and {max_val}." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "    Please enter a valid number." + Style.RESET_ALL)


def _input_choice(prompt: str, choices: list[str]) -> str:
    while True:
        val = input(prompt).strip().lower()
        if val in choices:
            return val
        print(Fore.RED + f"    Must be one of: {', '.join(choices)}." + Style.RESET_ALL)


def _input_symptoms(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if len(val) < 10:
            print(Fore.RED + "    Please describe your symptoms in more detail (min 10 characters)." + Style.RESET_ALL)
        elif len(val) > 1000:
            print(Fore.RED + "    Too long — please keep it under 1000 characters." + Style.RESET_ALL)
        else:
            return val


async def run_recommend():
    header("Med360 — Specialist Recommender")

    print(Style.BRIGHT + "\n  Tell us about the patient:\n")
    age      = _input_int("    Age                    : ", 1, 120)
    gender   = _input_choice("    Gender (male/female/other): ", ["male", "female", "other"])
    severity = _input_choice("    Severity (low/medium/high): ", ["low", "medium", "high"])
    duration = _input_int("    Duration (days)        : ", 1, 3650)
    symptoms = _input_symptoms("    Symptoms               : ")

    patient_info = build_patient_info(age, gender, severity, duration, symptoms)

    print()
    spinner = asyncio.create_task(animate_analyzing())
    try:
        data, model_used, usage_entry, session_id = await get_recommendation(patient_info)
    except RuntimeError as e:
        spinner.cancel()
        print(Fore.RED + f"\n  Error: {e}")
        return
    finally:
        spinner.cancel()
        sys.stdout.write("\r" + " " * 20 + "\r")

    urgency_color = URGENCY_COLOR.get(data.urgency_level, "")
    step_color    = STEP_COLOR.get(data.next_step, "")

    section("Recommendation")
    row("Specialist",   data.recommended_specialist)
    row("Urgency",      data.urgency_level.upper(), urgency_color)
    row("Next Step",    data.next_step.replace("_", " ").upper(), step_color)

    section("What This May Mean")
    for line in _wrap(data.symptom_explanation, 44):
        print("  " + line)

    section("Summary")
    for line in _wrap(data.primary_recommendation_summary, 44):
        print("  " + line)

    section("Specialist Pathway")
    for i, item in enumerate(data.specialist_pathway, 1):
        print(f"  {Style.BRIGHT}{i}. {item.specialist}{Style.RESET_ALL}")
        for line in _wrap(item.reason, 42):
            print(f"     {line}")

    section("Red Flags — Seek Emergency Care If:")
    for flag in data.red_flags:
        print(f"  {Fore.RED}•{Style.RESET_ALL} {flag}")

    section("Disclaimer")
    for line in _wrap(data.disclaimer, 44):
        print("  " + Fore.WHITE + Style.DIM + line + Style.RESET_ALL)

    section("Usage")
    row("Session ID",     session_id)
    row("Model",          model_used)
    row("Tokens",
        f"{usage_entry.get('total_tokens')} "
        f"(prompt: {usage_entry.get('prompt_tokens')}, "
        f"completion: {usage_entry.get('completion_tokens')})")
    row("Cost this call", f"${usage_entry.get('cost_usd', 0):.6f}")

    totals = get_session_totals()
    row("Session totals",
        f"{totals['total_requests']} request(s) | "
        f"{totals['total_tokens']} tokens | "
        f"${totals['total_cost_usd']:.6f}")
    print()


def _render_recommendation(data) -> None:
    urgency_color = URGENCY_COLOR.get(data.urgency_level, "")
    step_color    = STEP_COLOR.get(data.next_step, "")

    print()
    print(Style.BRIGHT + Fore.CYAN + "  " + "=" * 52 + Style.RESET_ALL)
    print(Style.BRIGHT + "  Specialist Recommendation")
    print(Style.BRIGHT + Fore.CYAN + "  " + "=" * 52 + Style.RESET_ALL)

    section("Recommendation")
    row("Specialist",   data.recommended_specialist)
    row("Urgency",      data.urgency_level.upper(), urgency_color)
    row("Next Step",    data.next_step.replace("_", " ").upper(), step_color)

    section("What This May Mean")
    for line in _wrap(data.symptom_explanation, 44):
        print("  " + line)

    section("Summary")
    for line in _wrap(data.primary_recommendation_summary, 44):
        print("  " + line)

    section("Specialist Pathway")
    for i, item in enumerate(data.specialist_pathway, 1):
        print(f"  {Style.BRIGHT}{i}. {item.specialist}{Style.RESET_ALL}")
        for line in _wrap(item.reason, 42):
            print(f"     {line}")

    section("Red Flags -- Seek Emergency Care If:")
    for flag in data.red_flags:
        print(f"  {Fore.RED}*{Style.RESET_ALL} {flag}")

    section("Disclaimer")
    for line in _wrap(data.disclaimer, 44):
        print("  " + Fore.WHITE + Style.DIM + line + Style.RESET_ALL)

    print()
    print(Style.BRIGHT + Fore.CYAN + "  " + "=" * 52 + Style.RESET_ALL)
    print()


def _wrap(text: str, width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


URGENCY_REPORT_COLOR = {
    "routine": Fore.GREEN,
    "soon":    Fore.YELLOW,
    "urgent":  Fore.RED + Style.BRIGHT,
}


async def run_interpret():
    header("Med360 — Report Interpreter")

    print(Style.BRIGHT + "\n  Enter the path to your report (PDF or TXT):\n")
    while True:
        raw = input("    File path: ").strip().strip('"').strip("'")
        path = Path(raw)
        if not path.exists():
            print(Fore.RED + f"    File not found: {raw}" + Style.RESET_ALL)
        elif path.suffix.lower() not in {".pdf", ".txt"}:
            print(Fore.RED + "    Only .pdf and .txt files are supported." + Style.RESET_ALL)
        else:
            break

    content_type = "application/pdf" if path.suffix.lower() == ".pdf" else "text/plain"

    print()
    spinner = asyncio.create_task(animate_analyzing())
    try:
        findings, model_used, usage_entry, report_id = await interpret_report(
            file_path=str(path),
            content_type=content_type,
            filename=path.name,
        )
    except (ValueError, NotImplementedError) as e:
        spinner.cancel()
        print(Fore.RED + f"\n  Error: {e}")
        return
    except RuntimeError as e:
        spinner.cancel()
        print(Fore.RED + f"\n  Error: {e}")
        return
    finally:
        spinner.cancel()
        sys.stdout.write("\r" + " " * 20 + "\r")

    urgency_color = URGENCY_REPORT_COLOR.get(findings.urgency, "")

    section("Report Overview")
    row("Report Type", findings.report_type)
    row("Test Date",   findings.test_date or "Not found in report")
    row("Urgency",     findings.urgency.upper(), urgency_color)

    if findings.abnormal_values:
        section("Abnormal Values")
        for lv in findings.abnormal_values:
            status_color = Fore.RED if lv.status == "abnormal" else Fore.YELLOW
            print(f"  {status_color}{Style.BRIGHT}{lv.name}{Style.RESET_ALL}  "
                  f"{lv.value} {lv.unit or ''}  "
                  f"(ref: {lv.reference_range or 'N/A'})")
            for line in _wrap(lv.plain_meaning, 44):
                print("    " + line)

    if findings.notable_markers:
        section("Notable Markers")
        for marker in findings.notable_markers:
            print(f"  {Fore.CYAN}*{Style.RESET_ALL} {marker}")

    section("Summary")
    for line in _wrap(findings.overall_summary, 44):
        print("  " + line)

    section("What This Means For You")
    for line in _wrap(findings.plain_explanation, 44):
        print("  " + line)

    section("Recommended Action")
    for line in _wrap(findings.recommended_action, 44):
        print(f"  {urgency_color}{line}{Style.RESET_ALL}")

    section("Usage")
    row("Report ID",     report_id)
    row("Model",         model_used)
    row("Tokens",
        f"{usage_entry.get('total_tokens')} "
        f"(prompt: {usage_entry.get('prompt_tokens')}, "
        f"completion: {usage_entry.get('completion_tokens')})")
    row("Cost this call", f"${usage_entry.get('cost_usd', 0):.6f}")
    print()


CHAT_URGENCY_COLOR = {
    "none":      "",
    "low":       Fore.GREEN,
    "moderate":  Fore.YELLOW,
    "high":      Fore.RED,
    "emergency": Fore.RED + Style.BRIGHT,
}

CHAT_STEP_LABEL = {
    "none":       "",
    "monitor":    "Monitor at home",
    "teleconsult": "Book a teleconsult",
    "home_visit": "Request a home visit",
    "specialist": "See a specialist",
    "emergency":  "Go to ER / call emergency services",
}


async def run_chat():
    header("Med360 — Medi Chat Assistant")

    chat_id = start_chat()
    print(Style.BRIGHT + f"\n  Chat ID : {chat_id}")
    print(f"  Commands: {Fore.CYAN}report <path>{Style.RESET_ALL} to load a report  |  "
          f"{Fore.CYAN}quit{Style.RESET_ALL} to exit\n")
    print(Fore.WHITE + Style.DIM + "  " + "─" * 52 + Style.RESET_ALL)

    report_loaded = False

    while True:
        try:
            user_input = input(f"\n  {Style.BRIGHT}You:{Style.RESET_ALL} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print(f"\n  {Fore.CYAN}Medi:{Style.RESET_ALL} Take care! Remember to follow up with your doctor. Goodbye.")
            break

        # ── report <path> command ──────────────────────────────────────────────
        if user_input.lower().startswith("report "):
            raw_path = user_input[7:].strip().strip('"').strip("'")
            path = Path(raw_path)
            if not path.exists():
                print(f"  {Fore.RED}File not found: {raw_path}{Style.RESET_ALL}")
                continue
            content_type = "application/pdf" if path.suffix.lower() == ".pdf" else "text/plain"
            print(f"  {Fore.CYAN}Interpreting report...{Style.RESET_ALL}")
            spinner = asyncio.create_task(animate_analyzing())
            try:
                findings, _, _, report_id = await interpret_report(str(path), content_type, path.name)
            except Exception as e:
                spinner.cancel()
                sys.stdout.write("\r" + " " * 20 + "\r")
                print(f"  {Fore.RED}Could not interpret report: {e}{Style.RESET_ALL}")
                continue
            finally:
                spinner.cancel()
                sys.stdout.write("\r" + " " * 20 + "\r")

            chat_attach_report(chat_id, report_id)
            report_loaded = True
            print(f"  {Fore.GREEN}Report loaded:{Style.RESET_ALL} {findings.report_type} "
                  f"({findings.urgency})")
            print(f"  You can now ask Medi questions about your report.\n")
            continue

        # ── normal message ─────────────────────────────────────────────────────
        spinner = asyncio.create_task(animate_analyzing())
        try:
            turn, _, usage, recommendation = await send_message(chat_id, user_input)
        except Exception as e:
            spinner.cancel()
            sys.stdout.write("\r" + " " * 20 + "\r")
            print(f"  {Fore.RED}Error: {e}{Style.RESET_ALL}")
            continue
        finally:
            spinner.cancel()
            sys.stdout.write("\r" + " " * 20 + "\r")

        # ── emergency banner ───────────────────────────────────────────────────
        if turn.urgency_level == "emergency" and turn.escalation_note:
            print()
            print(Fore.RED + Style.BRIGHT + "  !" * 22)
            print(f"  EMERGENCY: {turn.escalation_note}")
            print(Fore.RED + Style.BRIGHT + "  !" * 22)

        # ── response ───────────────────────────────────────────────────────────
        print()
        print(f"  {Style.BRIGHT}{Fore.CYAN}Medi:{Style.RESET_ALL}")
        print()
        for para in turn.message.split("\n"):
            para = para.strip()
            if not para:
                print()
                continue
            for line in _wrap(para, 68):
                print(f"    {line}")

        # ── metadata footer ────────────────────────────────────────────────────
        print()
        if turn.urgency_level != "none":
            u_color = CHAT_URGENCY_COLOR.get(turn.urgency_level, "")
            step_label = CHAT_STEP_LABEL.get(turn.suggested_next_step, "")
            badge = f"{u_color}[{turn.urgency_level.upper()}]{Style.RESET_ALL}"
            suggestion = f"  ->  {step_label}" if step_label else ""
            print(f"  {badge}{suggestion}")

        if turn.escalation_note and turn.urgency_level != "emergency":
            print(f"  {Fore.YELLOW}Note: {turn.escalation_note}{Style.RESET_ALL}")

        print(Fore.WHITE + Style.DIM +
              f"  tokens: {usage.get('total_tokens', 0)}  "
              f"cost: ${usage.get('cost_usd', 0):.5f}" +
              Style.RESET_ALL)
        print(Fore.WHITE + Style.DIM + "  " + "─" * 52 + Style.RESET_ALL)

        if recommendation:
            _render_recommendation(recommendation)


def main():
    parser = argparse.ArgumentParser(description="Med360 Patient AI -- CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("recommend", help="One-shot specialist recommendation")
    subparsers.add_parser("interpret", help="Interpret a medical report (PDF or TXT)")
    subparsers.add_parser("chat", help="Conversational chat with Medi (includes report Q&A)")

    args = parser.parse_args()
    if args.command == "recommend":
        asyncio.run(run_recommend())
    elif args.command == "interpret":
        asyncio.run(run_interpret())
    elif args.command == "chat":
        asyncio.run(run_chat())


if __name__ == "__main__":
    main()
