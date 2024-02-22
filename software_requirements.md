## Software Requirements

Website - Stack Overflow

### User Personas

All Users:
- **Why Stack Overflow?**
	- Asking Questions
	- Answering Questions
	- Reading Discussions
	- Follow others.

- **Aspirations**
	- To get the solutions to the problems.
	- To give answers to the problems that are know to me.

High Reputation Users:
- **Why Stack Overflow?**
	- Flagging the question and answers.
	- Voting the questions and answers.
	- Commenting the question or answer.
	- protect the question.

- **Aspirations**
	- To teach the knowledge they have.
    - To make the answer to be more efficent.


### User Stories

As a General User, ISBAT to check the questions.<br>
As a General User, ISBAT to post a question.<br>
As a General User, ISBAT to answer the question.<br>
As a General User, ISBAT to accept the answer.<br>
As a General User, ISBAT to save a question.<br>
As a General User, ISBAT to save a answer.<br>
As a General User, ISBAT to follow others.<br>

As a Higher Reputation Users, ISBAT to comment.<br>
As a Higher Reputation Users, ISBAT to flag the question.<br>
As a Higher Reputation Users, ISBAT to flag the answer.<br>
As a Higher Reputation Users, ISBAT to vote the question.<br>
As a Higher Reputation Users, ISBAT to vote the answer.<br>
As a Higher Reputation Users, ISBAT to protect the question.<br>


### Database Design

- **User**
	- Id
	- Name
	- Joined date
	- Profile Picture
	- Reputation
  
- **Questions**
	- Id
	- User Id
	- Title
	- Content
	- votes
	- posted date
	- modified date
	- accepted answer

- **Answers**
    - Id
    - Question Id
    - User Id
    - Content
    - votes
    - posted date
    - modified date

- **Follwers**
    - Id 
    - User Id
    - Following User Id

- **Question Comments**
    - Id
    - User Id
    - Question Id
    - Content

- **Answer Comments**
	- Id
    - User Id
    - Answer Id
    - Content