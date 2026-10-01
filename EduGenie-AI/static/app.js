"use strict";


const task = document.getElementById("task");

const userInput = document.getElementById("userInput");

const levelContainer =
    document.getElementById("levelContainer");

const level =
    document.getElementById("level");

const submitButton =
    document.getElementById("submitButton");

const buttonText =
    document.getElementById("buttonText");

const spinner =
    document.getElementById("spinner");

const status =
    document.getElementById("status");

const resultContainer =
    document.getElementById("resultContainer");

const result =
    document.getElementById("result");

const copyButton =
    document.getElementById("copyButton");


const API_ENDPOINTS = {

    qa: "/qa",

    explain: "/explain",

    quiz: "/quiz",

    summarize: "/summarize",

    learn: "/learn/recommendations"

};


const PLACEHOLDERS = {

    qa:
        "Example: What is the largest ocean in the world?",

    explain:
        "Example: Explain the Pythagoras theorem in simple language.",

    quiz:
        "Paste a topic or educational passage here to generate 3 MCQs.",

    summarize:
        "Paste the educational passage you want to summarize.",

    learn:
        "Example: SQL, Python, Machine Learning, Web Development..."

};


const BUTTON_TEXT = {

    qa: "Ask EduGenie",

    explain: "Explain Concept",

    quiz: "Generate Quiz",

    summarize: "Summarize",

    learn: "Create Learning Path"

};


function updateTaskUI() {

    const selectedTask = task.value;

    userInput.placeholder =
        PLACEHOLDERS[selectedTask];

    buttonText.textContent =
        BUTTON_TEXT[selectedTask];

    if (selectedTask === "learn") {

        levelContainer.classList.remove(
            "hidden"
        );

    } else {

        levelContainer.classList.add(
            "hidden"
        );

    }

}


task.addEventListener(
    "change",
    updateTaskUI
);


function setLoading(isLoading) {

    submitButton.disabled = isLoading;

    spinner.classList.toggle(
        "hidden",
        !isLoading
    );

    if (isLoading) {

        buttonText.textContent =
            "Generating...";

        status.textContent =
            "EduGenie is thinking...";

    } else {

        buttonText.textContent =
            BUTTON_TEXT[task.value];

    }

}


function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


function formatText(text) {

    let safe = escapeHTML(text);

    safe = safe.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    safe = safe.replace(
        /^### (.*)$/gm,
        "<h3>$1</h3>"
    );

    safe = safe.replace(
        /^## (.*)$/gm,
        "<h2>$1</h2>"
    );

    safe = safe.replace(
        /^# (.*)$/gm,
        "<h1>$1</h1>"
    );

    safe = safe.replace(
        /^[-*] (.*)$/gm,
        "<li>$1</li>"
    );

    safe = safe.replace(
        /(<li>.*<\/li>)/gs,
        "<ul>$1</ul>"
    );

    safe = safe.replace(
        /\n\n/g,
        "</p><p>"
    );

    safe =
        "<p>" +
        safe +
        "</p>";

    return safe;

}


function renderQuiz(questions) {

    result.innerHTML = "";

    let score = 0;

    let answered = 0;

    const wrapper =
        document.createElement("div");

    questions.forEach(
        (question, questionIndex) => {

            const questionBox =
                document.createElement("div");

            questionBox.className =
                "quiz-question";

            const heading =
                document.createElement("h3");

            heading.textContent =
                `${questionIndex + 1}. ${question.question}`;

            questionBox.appendChild(
                heading
            );


            const explanation =
                document.createElement("div");

            explanation.className =
                "quiz-explanation hidden";

            explanation.textContent =
                question.explanation ||
                "Review the concept and try again.";

            question.options.forEach(
                (option) => {

                    const optionButton =
                        document.createElement("button");

                    optionButton.className =
                        "quiz-option";

                    optionButton.textContent =
                        option;


                    optionButton.addEventListener(
                        "click",
                        () => {

                            if (
                                questionBox.dataset.answered
                            ) {
                                return;
                            }


                            questionBox.dataset.answered =
                                "true";

                            answered++;


                            const buttons =
                                questionBox.querySelectorAll(
                                    ".quiz-option"
                                );


                            buttons.forEach(
                                (button) => {

                                    if (
                                        button.textContent ===
                                        question.answer
                                    ) {

                                        button.classList.add(
                                            "correct"
                                        );

                                    }

                                }
                            );


                            if (
                                option ===
                                question.answer
                            ) {

                                score++;

                            } else {

                                optionButton.classList.add(
                                    "wrong"
                                );

                            }


                            explanation.classList.remove(
                                "hidden"
                            );


                            if (
                                answered ===
                                questions.length
                            ) {

                                scoreBox.textContent =
                                    `Score: ${score}/${questions.length}`;

                            }

                        }
                    );


                    questionBox.appendChild(
                        optionButton
                    );

                }
            );


            questionBox.appendChild(
                explanation
            );


            wrapper.appendChild(
                questionBox
            );

        }
    );


    const scoreBox =
        document.createElement("div");

    scoreBox.className =
        "quiz-score";

    scoreBox.textContent =
        "Answer all questions to see your score.";

    wrapper.appendChild(
        scoreBox
    );


    result.appendChild(
        wrapper
    );

}


function buildRequestBody(selectedTask, text) {

    if (selectedTask === "qa") {

        return {
            question: text
        };

    }


    if (selectedTask === "explain") {

        return {
            topic: text
        };

    }


    if (selectedTask === "quiz") {

        return {
            text: text
        };

    }


    if (selectedTask === "summarize") {

        return {
            text: text
        };

    }


    if (selectedTask === "learn") {

        return {
            topic: text,
            level: level.value
        };

    }


    throw new Error(
        "Unknown task selected."
    );

}


async function submitRequest() {

    const selectedTask =
        task.value;

    const text =
        userInput.value.trim();


    if (!text) {

        status.textContent =
            "Please enter some content first.";

        resultContainer.classList.add(
            "hidden"
        );

        userInput.focus();

        return;

    }


    setLoading(true);

    resultContainer.classList.add(
        "hidden"
    );


    try {

        const response =
            await fetch(
                API_ENDPOINTS[selectedTask],
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        buildRequestBody(
                            selectedTask,
                            text
                        )
                    )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );

        }


        resultContainer.classList.remove(
            "hidden"
        );


        if (
            selectedTask === "quiz"
        ) {

            renderQuiz(
                data.questions
            );

        } else {

            result.innerHTML =
                formatText(
                    data.result
                );

        }


        status.textContent =
            "Completed successfully.";

        resultContainer.scrollIntoView(
            {
                behavior: "smooth",
                block: "start"
            }
        );


    } catch (error) {

        status.textContent =
            error.message ||
            "Request failed.";

        result.innerHTML = "";

        resultContainer.classList.remove(
            "hidden"
        );


        const errorBox =
            document.createElement("p");

        errorBox.textContent =
            error.message ||
            "Unable to generate a response.";

        errorBox.style.color =
            "#ff6577";

        result.appendChild(
            errorBox
        );

    } finally {

        setLoading(false);

    }

}


submitButton.addEventListener(
    "click",
    submitRequest
);


userInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            (event.ctrlKey || event.metaKey)
        ) {

            submitRequest();

        }

    }
);


copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );

            copyButton.textContent =
                "Copied!";

            setTimeout(
                () => {
                    copyButton.textContent =
                        "Copy";
                },
                1500
            );

        } catch {

            copyButton.textContent =
                "Copy failed";

        }

    }
);


updateTaskUI();