from behave import given, then, when

from src.main import Jogo
import pygame as pg


def post_and_next_frame(event, wrapper):
    pg.event.post(event)
    next(wrapper)


@given("I run the game")
def step_run_the_game(context):
    context.game = Jogo()
    context.wrapper = context.game.novo()
    next(context.wrapper)


@then("the game is running")
def step_assert_running(context):
    assert context.game.jogando == True


@when("I close the game")
def step_close_the_game(context):
    try:
        event = pg.event.Event(pg.QUIT)
        post_and_next_frame(event, context.wrapper)
    except StopIteration:
        pass


@then("the game window is closed")
def step_assert_game_is_closed(context):
    assert context.game.jogando == False
