# source: https://blog.codemanship.dev/how-to-feature-test-your-pygame-game

Feature: Opening and closing the game

    Scenario: Opening the game 
              Given I run the game 
              Then the game is running

    Scenario: Closing the game 
              Given I run the game 
              When I close the game 
              Then the game window is closed
