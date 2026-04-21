import asyncio
import argparse
import sys
import itertools
from colorama import init, Fore, Style

from app.services.llm import build_patient_info, get_recommendation
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


def main():
    parser = argparse.ArgumentParser(description="Med360 Patient AI — CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("recommend", help="Interactive specialist recommendation")

    args = parser.parse_args()
    if args.command == "recommend":
        asyncio.run(run_recommend())


if __name__ == "__main__":
    main()
