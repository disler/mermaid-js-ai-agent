# This graph illustrates a simple relationship between nodes A, B, C, D, and E, showing how each node is connected to others.
graph = """
graph LR;
    A--> B & C & D;
    B--> A & E;
    C--> A & E;
    D--> A & E;
    E--> B & C & D;
"""

# This pie chart illustrates sales by product, with Product A accounting for 40%, Product B for 30%, Product C for 20%, and Product D for 10%.
pie_chart = """
pie
    title Sales by Product
    "Product A": 40
    "Product B": 30
    "Product C": 20
    "Product D": 10
"""

# This sequence diagram illustrates a conversation between Alice and Bob, with a loop for John's healthcheck.
sequence_diagram = """
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
"""

# This Gantt chart illustrates a project schedule with two sections, showing the start date, duration, and completion status of tasks.
gantt_chart = """
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task     : 24d
"""

# This class diagram illustrates an Animal hierarchy with Duck, Fish, and Zebra subclasses, showing their attributes and methods.
class_diagram = """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
"""
