/*
 * The contract deployed on this address is Logger
 */

pragma solidity =0.4.25;

contract Logger{
    event WeHaveAWinner(address);
    event NewQuestion(string);
    event NewAnswerHs(bytes32);
    function AcoraidaMonicaWantsToKeepALogOfTheWinner(address winner) public {
        emit WeHaveAWinner(winner);
    }
    function AcoraidaMonicaWantsToKnowTheNewQuestion(string _question) public{
        emit NewQuestion(_question);
    }
    function AcoraidaMonicaWantsToKnowTheNewAnswerHash(bytes32 _answerHash) public {
        emit NewAnswerHs(_answerHash);
    }
}
