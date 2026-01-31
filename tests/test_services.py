import pytest
from services import DataProcessor, calculate_summary, validate_input, process_data

@pytest.mark.parametrize("input_data, expected", [
    ({"key": "value"}, True),
    ({"key": 123}, True),
    (None, False),
    ([], False),
    ("invalid", False),
    ({}, False),
])
def test_validate_input(input_data, expected):
    assert validate_input(input_data) == expected

@pytest.mark.parametrize("input_data, expected", [
    ({"key": "value"}, {"processed_key": "value"}),
    ({"key": 123}, {"processed_key": 123}),
    ([1, 2, 3], [1, 2, 3]),
    (None, None),
    ("invalid", "invalid"),
])
def test_process_data(input_data, expected):
    result = process_data(input_data)
    assert result == expected

@pytest.mark.parametrize("data, expected", [
    ([1, 2, 3], 6),
    ([], 0),
    ([10], 10),
    (["a", "b"], "ab"),
    ({"a": 1}, 1),
])
def test_calculate_summary(data, expected):
    assert calculate_summary(data) == expected

def test_data_processor_initialization():
    processor = DataProcessor()
    assert hasattr(processor, "processed_data")
    assert processor.processed_data is None

def test_data_processor_process_valid_data():
    processor = DataProcessor()
    processor.process_data({"key": "value"})
    assert processor.processed_data == {"processed_key": "value"}

def test_data_processor_process_invalid_data():
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.process_data(None)

def test_data_processor_multiple_processing_steps():
    processor = DataProcessor()
    processor.process_data({"key": "value"})
    processor.process_data({"key": 123})
    assert processor.processed_data == {"processed_key": 123}

def test_data_processor_invalid_data_type():
    processor = DataProcessor()
    with pytest.raises(TypeError):
        processor.process_data(123)

def test_data_processor_empty_data():
    processor = DataProcessor()
    processor.process_data([])
    assert processor.processed_data == []

def test_data_processor_string_data():
    processor = DataProcessor()
    processor.process_data("test")
    assert processor.processed_data == "test"

def test_data_processor_nested_data():
    processor = DataProcessor()
    processor.process_data({"key": {"subkey": "value"}})
    assert processor.processed_data == {"processed_key": {"processed_subkey": "value"}}

def test_data_processor_invalid_nested_data():
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.process_data({"key": [1, 2, 3]})

def test_data_processor_error_handling():
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.process_data({"invalid_key": "value"})

def test_data_processor_custom_error():
    processor = DataProcessor()
    with pytest.raises(ValueError, match="Invalid data format"):
        processor.process_data({"key": [1, 2, 3]})

def test_data_processor_edge_case():
    processor = DataProcessor()
    processor.process_data({"key": ""})
    assert processor.processed_data == {"processed_key": ""}