from project_1.formula_1.models import Constructor


def test_constructor(constructor_data):

    # Arrange
    

    # Act
    constructor: Constructor = Constructor.from_dict(constructor_data)

    # Assert
    assert constructor.id == "1"

