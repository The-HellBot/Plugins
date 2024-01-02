# HellBot v3 Plugins

# Follow this format to make your own plugin for HellBot.

```python3
"""
A sample code to display hello without taking input.
"""
# this is a mandatory import
from . import on_message, hellbot, HelpMenu

# assigning command
@on_message("hii")
async def hi(_, message):
    # command body
    await hellbot.edit(message, "Hello!")


# to display in help menu
HelpMenu("hii").add(
  "hii", None, "Says Hello!"
).done()
```

```python3
"""
A sample code to display hello with input.
"""
# this is a mandatory import
from . import on_message, hellbot, HelpMenu

# assigning command
@on_message("hii", allow_stan=True)
async def hi(_, message):
    # command body
    msg = await hellbot.input(message)
    if msg:
        await hellbot.edit(message, f"Hello! {msg}")
    else:
        await hellbot.edit(message, "Hello!")


# to display in help menu
HelpMenu("hii").add(
    "hii", "<text>", "Display Hello with a input!"
).done()
```


## To get more functions read codes in repo.
