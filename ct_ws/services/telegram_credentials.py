from sqlalchemy.ext.asyncio import AsyncSession

from ct_ws.db.models.user_telegram_credentials import UserTelegramCredentials


class TelegramCredentialsService:
    """The TelegramCredentialsService class."""

    @staticmethod
    async def create_telegram_credentials(
        session: AsyncSession,
        user_id: int,
        telegram_id: int,
        telegram_username: str,
    ) -> UserTelegramCredentials:
        """
        Create a new telegram credentials object.

        The create_telegram_credentials function creates a new UserTelegramCredentials
        and adds it to the database.

        :param session: AsyncSession: Access the database
        :param user_id: int: Identify the user
        :param telegram_id: int: Identify the user in telegram
        :param telegram_username: str: Store the username of the user
        :return: A usertelegramcredentials object
        :rtype: UserTelegramCredentials
        :doc-author: Trelent
        """
        telegram_credentials = UserTelegramCredentials(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            user_id=user_id,
        )
        session.add(telegram_credentials)
        return telegram_credentials
