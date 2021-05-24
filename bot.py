from botbuilder.dialogs import Dialog
from models.user_emotion_at_checkin import UserEmotionAtCheckIn
from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes
from helpers.dialog_helper import DialogHelper


class MyBot(ActivityHandler):
    def __init__(
            self,
            conversation_state: ConversationState,
            user_state: UserState,
            dialog: Dialog,
        ):
            if conversation_state is None:
                raise TypeError(
                    "[DialogBot]: Missing parameter. conversation_state is required but None was given"
                )
            if user_state is None:
                raise TypeError(
                    "[DialogBot]: Missing parameter. user_state is required but None was given"
                )
            if dialog is None:
                raise Exception("[DialogBot]: Missing parameter. dialog is required")

            self.conversation_state = conversation_state
            self.user_state = user_state
            self.dialog = dialog


    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                curr_user = await self.user_state.user_profile_accessor.get(
                    turn_context, UserEmotionAtCheckIn
                )
                curr_user.set_username(member.name)
                curr_user.set_userid(member.id)
                message = Activity(
                    text=f"Hello {curr_user.name}! Let's check in! (Type anything to begin)",
                    type=ActivityTypes.message
                )
                await turn_context.send_activity(message)

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
