"""Safe arithmetic calculator command."""
from . import *
from Eivabot.utils.safe_math import evaluate


@bot.on(Eiva_cmd(pattern=r"calc\s+(.+)"))
@bot.on(sudo_cmd(pattern=r"calc\s+(.+)", allow_sudo=True))
async def calculate(event):
    if event.fwd_from:
        return
    expression = event.pattern_match.group(1).strip()
    try:
        result = evaluate(expression)
        response = f"**EQUATION**: `{expression}`\n\n**SOLUTION**: `{result}`"
    except (SyntaxError, ValueError, ArithmeticError) as exc:
        response = f"Could not calculate that expression: `{exc}`"
    await edit_or_reply(event, response)


CmdHelp("calc").add_command(
    "calc", "expression", "Evaluates a numeric arithmetic expression."
).add_info("Safe arithmetic calculator").add()
