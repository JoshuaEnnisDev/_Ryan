function checkAnswers(event) {
  event.preventDefault()
  const form = document.getElementById('quizForm');

  // Hardcoded correct answers for each question
  const correctAnswers = {
      q1: 'a',  // Correct answer for Question 1
      q2: 'b',  // Correct answer for Question 2
      // Add more correct answers as needed
  };

  let score = 0;

  // Loop through each question in the form
  for (const question in correctAnswers) {
      // Get the user's answer for the current question
      const userAnswer = form.elements[question].value;
      const correctAnswer = correctAnswers[question];

      console.log(`Question: ${question}, User Answer: ${userAnswer}, Correct Answer: ${correctAnswer}`);

      // Check if the user's answer matches the correct answer
      if (userAnswer === correctAnswer) {
          score++;
      }
  }

  // Display the score on the page
  const scoreElement = document.getElementById('score');
  scoreElement.textContent = `Score: ${score}`;
}
