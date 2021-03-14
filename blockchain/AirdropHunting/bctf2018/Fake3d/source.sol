contract WinnerList{
    address public owner;
    struct Richman{
        address who;
        uint balance;
    }

    function note(address _addr, uint _value) public{
        Richman rm;
        rm.who = _addr;
        rm.balance = _value;
    }

}

contract Fake3D {
    using SafeMath for *;
    mapping(address => uint256)  public balance;
    uint public totalSupply  = 10**18;
    WinnerList wlist;

    event FLAG(string b64email, string slogan);

    constructor(address _addr) public{
        wlist = WinnerList(_addr);
    }

    modifier turingTest() {
            address _addr = msg.sender;
            uint256 _codeLength;
            assembly {_codeLength := extcodesize(_addr)}
            require(_codeLength == 0, "sorry humans only");
            _;
    }

    function transfer(address _to, uint256 _amount) public{
        require(balance[msg.sender] >= _amount);
        balance[msg.sender] = balance[msg.sender].sub(_amount);
        balance[_to] = balance[_to].add(_amount);
    }


    function airDrop() public turingTest returns (bool) {
        uint256 seed = uint256(keccak256(abi.encodePacked(
            (block.timestamp).add
            (block.difficulty).add
            ((uint256(keccak256(abi.encodePacked(block.coinbase)))) / (now)).add
            (block.gaslimit).add
            ((uint256(keccak256(abi.encodePacked(msg.sender)))) / (now)).add
            (block.number)
        )));

        if((seed - ((seed / 1000) * 1000)) < 288){
            balance[tx.origin] = balance[tx.origin].add(10);
            totalSupply = totalSupply.sub(10);
            return true;
        }
        else
            return false;
    }

   function CaptureTheFlag(string b64email) public{
        require (balance[msg.sender] > 8888);
        wlist.note(msg.sender,balance[msg.sender]);
        emit FLAG(b64email, "Congratulations to capture the flag?");
    }

}
