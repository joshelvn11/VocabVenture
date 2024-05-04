import { setFlashcardData } from "../flashcards";

describe("setFlashcardData function", () => {
  // Mocking jQuery global object and its methods
  global.$ = jest.fn(() => ({
    text: jest.fn(),
    on: jest.fn(),
    off: jest.fn(),
    addClass: jest.fn(),
    removeClass: jest.fn(),
    prop: jest.fn(),
  }));

  const mockFlashcardData = [
    {
      title: "Card Title",
      question: "What is the capital of France?",
      answer: "Paris",
      "question-roman": "Paris",
      "answer-roman": "Paris",
      "question-pronounciation": "Paris",
      "answer-pronounciation": "Paris",
      "question-pronounciation-audio": "sound.m4a",
      "answer-pronounciation-audio": "sound.m4a",
    },
  ];

  beforeEach(() => {
    // Resetting all mocks before each test
    $.mockClear();
  });

  test("should set correct texts for flashcard elements", () => {
    setFlashcardData(mockFlashcardData);
    expect($.text).toHaveBeenCalledWith("Card Title");
    expect($.text).toHaveBeenCalledWith("What is the capital of France?");
    expect($.text).toHaveBeenCalledWith("Paris");
  });

  test("should handle visibility of romanisation and pronounciation buttons", () => {
    setFlashcardData(mockFlashcardData);
    expect($.removeClass).toHaveBeenCalledWith("hidden");
  });

  test("should attach event listeners for pronounciation and romanisation", () => {
    setFlashcardData(mockFlashcardData);
    expect($.on).toHaveBeenCalledTimes(4); // Two for show, two for audio play
  });

  test("should load and handle audio correctly for valid extensions", () => {
    const audioMock = {
      play: jest.fn(),
      onerror: jest.fn(),
    };
    window.Audio = jest.fn(() => audioMock);

    setFlashcardData(mockFlashcardData);
    expect(window.Audio).toHaveBeenCalledWith("sound.m4a");
    expect(audioMock.play).not.toHaveBeenCalled(); // Should not play without user interaction
  });

  test("should not attempt to load audio for invalid extensions", () => {
    const modifiedData = [
      {
        ...mockFlashcardData[0],
        "question-pronounciation-audio": "sound.invalid",
      },
    ];
    window.Audio = jest.fn();

    setFlashcardData(modifiedData);
    expect(window.Audio).not.toHaveBeenCalled();
  });
});
