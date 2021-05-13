import json
import os

from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes

CARDS = [
    "resources/EmotionPoll.json",
]
class MyBot(ActivityHandler):

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                message = Activity(
                    text=f"Hello {member.name}!",
                    type=ActivityTypes.message,
                    attachments=[self._create_adaptive_card_attachment()],
                )

                await turn_context.send_activity(message)

    def _create_adaptive_card_attachment(self) -> Attachment:
        card_path = os.path.join(os.getcwd(), CARDS[0])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)
