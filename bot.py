# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


import os
import openai
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, AzureCliCredential

keyVaultName = "aikvjcst"
KVUri = f"https://aikvjcst.vault.azure.net"

credential = AzureCliCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
retrieved_secret = client.get_secret("aoai")

openai.api_type = "azure"
openai.api_base = "https://azopenai-demo.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = retrieved_secret.value


class MyBot(ActivityHandler):
    ### This is an example. This is also really bad design.

    async def on_message_activity(self, turn_context: TurnContext):
        response = openai.ChatCompletion.create(
                engine="ChatGPT",
                messages = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":turn_context.activity.text}],
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None)
        print(response)
        await turn_context.send_activity(response.choices[0].message.content)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome to the Azure OpenAI Service Experience!")
