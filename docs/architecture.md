# Architecture Overview

This project is a single-file Pygame application centered on [main.py](../main.py). It initializes a window, creates a fixed population of square entities, and runs a frame loop that updates, redraws, and respawns squares until the user closes the window.

## Module Dependency Graph

```mermaid
graph TD
    main["main.py"]
    random["random"]
    math["math"]
    sys["sys"]
    pygame["pygame"]
    squareClass["Square"]
    distanceFn["distance()"]

    main --> random
    main --> math
    main --> sys
    main --> pygame
    main --> squareClass
    main --> distanceFn
    squareClass --> random
    squareClass --> math
    squareClass --> pygame
    distanceFn --> math
```

## Runtime Flow

```mermaid
flowchart TD
    A["Start program"] --> B["Initialize Pygame"]
    B --> C["Create 800x600 window and clock"]
    C --> D["Create 20 squares"]
    D --> E["Enter frame loop"]
    E --> F["Poll events"]
    F --> G{"Quit event?"}
    G -- "Yes" --> H["Stop running"]
    G -- "No" --> I["Fill background"]
    I --> J["Update each square"]
    J --> K["Remove expired squares"]
    K --> L{"Need more squares?"}
    L -- "Yes" --> M["Spawn new Square instances"]
    L -- "No" --> N["Draw all squares"]
    M --> N
    N --> O["Flip display and tick FPS"]
    O --> E
    H --> P["Quit Pygame and exit"]
```

## Function Call Graph

```mermaid
graph TD
    main_fn["main()"] --> pygame_init["pygame.init()"]
    main_fn --> set_mode["pygame.display.set_mode()"]
    main_fn --> set_caption["pygame.display.set_caption()"]
    main_fn --> clock_create["pygame.time.Clock()"]
    main_fn --> square_create["Square.__init__()"]
    main_fn --> event_get["pygame.event.get()"]
    main_fn --> update_call["Square.update()"]
    main_fn --> draw_call["Square.draw()"]
    main_fn --> flip_call["pygame.display.flip()"]
    main_fn --> tick_call["clock.tick()"]
    main_fn --> quit_call["pygame.quit()"]
    main_fn --> sys_exit["sys.exit()"]

    square_create --> rand_init["random.randint() / random.choice()"]
    update_call --> center_call["Square.center()"]
    update_call --> distance_call["distance()"]
    update_call --> hyp_call["math.hypot()"]
    update_call --> rand_update["random.random() / random.choice() / random.randint()"]
    draw_call --> rect_call["pygame.draw.rect()"]
    distance_call --> math_ops["basic arithmetic"]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as "User"
    participant M as "main()"
    participant P as "Pygame"
    participant E as "Event Queue"
    participant S as "Square"
    participant R as "Random / Math"

    U->>M: Launch program
    M->>P: init, create window, create clock
    M->>S: Create 20 Square instances

    loop Each frame at 60 FPS
        M->>E: Poll events
        alt Quit event received
            E-->>M: pygame.QUIT
            M->>P: quit
            M->>U: Exit program
        else Continue running
            M->>P: Fill background
            loop For each square
                M->>S: update(squares)
                S->>R: compute center, distance, and random fallback
                alt A larger square is nearby
                    S->>R: steer velocity toward threat
                else No threat nearby
                    S->>R: occasionally randomize direction
                end
                S->>S: move and bounce at window edges
            end
            M->>M: remove expired squares
            alt Population below target
                M->>S: spawn new Square instances
            end
            loop For each square
                M->>S: draw(surface)
                S->>P: draw rectangle
            end
            M->>P: flip display and cap frame rate
        end
    end
```

## Notes

- The runtime uses `SQUARE_COUNT = 20`, even though the README still mentions 10 squares.
- `Square.update()` combines local movement, edge bouncing, threat-seeking behavior, and lifespan decay in one step.
- The app is intentionally self-contained: there are no extra project modules beyond the main entry point and dependency file.
