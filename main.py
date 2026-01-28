from src.infrastructure.models.db.achievement import Achievement
from src.core.database import Base, session_maker
from sqlalchemy import inspect
from src.core.database import engine
from src.infrastructure.models.game.start_view import StartView
import arcade
from pyglet.image import load


# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"


def main():
    inspector = inspect(engine)
    base = "/mnt/d/projects/flappy_bird/src/assets/achievements/"

    if not inspector.get_table_names():
        Base.metadata.create_all(engine)
        with session_maker() as session:
            session.add(
                Achievement(
                    name="First Flight",
                    description="Pass your first pipe and take to the skies!",
                    icon_url=f"{base}1.png",
                )
            )
            session.add(
                Achievement(
                    name="Dozen",
                    description="Master the skies by passing 12 pipes in a single flight.",
                    icon_url=f"{base}2.png",
                )
            )
            session.add(
                Achievement(
                    name="Centurion",
                    description="Rack up a score of 100 points through skillful flying.",
                    icon_url=f"{base}3.png",
                )
            )
            session.add(
                Achievement(
                    name="Survivor",
                    description="Stay airborne for a full 60 seconds without crashing.",
                    icon_url=f"{base}4.png",
                )
            )
            session.add(
                Achievement(
                    name="Ghost Hunter",
                    description="Activate Ghost Mode to phase through obstacles at least once.",
                    icon_url=f"{base}5.png",
                )
            )
            session.add(
                Achievement(
                    name="Perfect Shield",
                    description="Turn on Shield and take zero damage during its full duration.",
                    icon_url=f"{base}6.png",
                )
            )
            session.add(
                Achievement(
                    name="Speed Demon",
                    description="Reach level 5 by surviving intense high-speed action.",
                    icon_url=f"{base}7.png",
                )
            )
            session.add(
                Achievement(
                    name="Powerup Master",
                    description="Collect 10 different types of powerups throughout your flights.",
                    icon_url=f"{base}8.png",
                )
            )

        session.commit()

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.icon = load("src/assets/favicon.ico")
    window.set_icon(window.icon)
    start_view = StartView(StartView)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
