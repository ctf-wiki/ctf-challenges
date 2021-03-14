/*
 * The contract deployed on this address is LoggerAgent
 */

pragma solidity =0.4.25;

contract LoggerAgent{
    bytes32 private constant ownerSlot = keccak256("Acoraida Monica is cute :P");
    bytes32 private constant implSlot = keccak256("So is her logger :D");
    constructor() public{
        setAddress(ownerSlot, msg.sender);
    }
    modifier onlyOwner{
        require(owner()==msg.sender);
        _;
    }
    function getAddress(bytes32 _slot) internal view returns (address value) {
        bytes32 s = _slot;
        assembly {value := sload(s)}
    }
    function setAddress(bytes32 _slot, address _address) internal {
        bytes32 s = _slot;
        assembly {sstore(s, _address)}
    }
    
    function owner() public view returns (address){
        return getAddress(ownerSlot);
    }
    function implementation() public view returns (address){
        return getAddress(implSlot);
    }

    function setOwner(address _owner) onlyOwner public{
        setAddress(ownerSlot, _owner);
    }
    function upgrade(address _impl) onlyOwner public {
        setAddress(implSlot, _impl);
    }

    function _delegateforward(address _impl) internal {
        assembly {
            calldatacopy(0, 0, calldatasize)
            let result := delegatecall(gas, _impl, 0, calldatasize, 0, 0)
            returndatacopy(0, 0, returndatasize)
            switch result
            case 0 {revert(0, returndatasize)}
            default {return(0, returndatasize)}
        }
    }
    function () payable public{
        _delegateforward(implementation());
    }
}
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
