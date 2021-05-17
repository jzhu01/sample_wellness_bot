from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    PromptOptions
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from models import UserEmotionAtCheckIn

class UserCheckinDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(UserCheckinDialog, self).__init__(UserCheckinDialog.__name__)
        self.user_state = user_state

        self.user_profile_accessor = self.user_state.create_property("UserEmotionAtCheckIn")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.icon_checkin_step,
                    self.choose_an_emotion_step,
                    self.get_context_step,
                    self.confirm_step,
                    self.summary_step
                ],
            )
        )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def icon_checkin_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Overall, How are you feeling right now?"),
                choices=[Choice("💚"), Choice("💛"), Choice("❤️")],
            ),
        )

    async def choose_an_emotion_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["icon"] = step_context.result.value

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Can you choose 1 emotion to summarize how you're feeling at this moment?"),
                choices=[
                    Choice("Happy"), Choice("Loving"), Choice("Relief"), Choice("Content"),
                    Choice("Amused"), Choice("Joy"), Choice("Proud"), Choice("Excited"),
                    Choice("Peaceful"), Choice("Satisfied"), Choice("Lonely"), Choice("Heartbroken"),
                    Choice("Gloomy"), Choice("Disappointed"), Choice("Hopeless"), Choice("Unhappy"),
                    Choice("Lost"), Choice("Troubled"), Choice("Miserable"), Choice("Resigned"),
                    Choice("Worried"), Choice("Doubtful"), Choice("Anxious"), Choice("Nervous"),
                    Choice("Terrified"), Choice("Panic"), Choice("Horrified"), Choice("Desperate"),
                    Choice("Confused"), Choice("Stressed"), Choice("Annoyed"), Choice("Frustrated"),
                    Choice("Bitter"), Choice("Infuriated"), Choice("Irritated"), Choice("Mad"),
                    Choice("Cheated"), Choice("Insulted"), Choice("Peeved"), Choice("Uncomfortable"),
                    Choice("Disturbed")
                ]
            ),
        )

    async def get_context_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["emotion"] = step_context.result.value.lower()
        emotion = step_context.result.value.lower()


        await step_context.context.send_activity(
            MessageFactory.text(f"Okay, so you're feeling {emotion}.")
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(f"Can you give some more context into why you feel {emotion}?")
            ),
        )

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["context"] = step_context.result

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Is this ok?")),
        )

    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.result:

            user_current_emotion = await self.user_profile_accessor.get(
                step_context.context, UserEmotionAtCheckIn
            )

            #todo: get the username and maybe profile pic from the channel
            user_current_emotion.icon = step_context.values["icon"]
            user_current_emotion.emotion = step_context.values["emotion"]
            user_current_emotion.context = step_context.values["context"]
            user_current_emotion.update_timestamp()

            #todo: might be good to set this up as an adaptive card to make it look nicer
            msg = f"I have your current icon set as {user_current_emotion.icon} and your emotion as {user_current_emotion.emotion}, with the context being: {user_current_emotion.context}."

            await step_context.context.send_activity(MessageFactory.text(msg))

            #todo: hook this up to a mongodb persistence

        else:
            # todo: find a way to restart the dialog here if the user chooses to continue
            await step_context.context.send_activity(
                MessageFactory.text("Thanks. Your profile will not be kept.")
            )

        return await step_context.end_dialog()