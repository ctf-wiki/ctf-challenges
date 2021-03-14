pragma solidity =0.6.12;
pragma experimental ABIEncoderV2;

interface IERC223 {
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address account) external view returns (uint);
    function transfer(address to, uint value) external returns (bool);
    function transfer(address to, uint value, bytes memory data) external returns (bool);
    function transfer(address to, uint value, bytes memory data, string memory customFallback) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint value, bytes data);
}

contract ERC223 is IERC223 {
    string public override name;
    string public override symbol;
    uint8 public override decimals;
    uint public override totalSupply;
    mapping (address => uint) private _balances;
    string private constant _tokenFallback = "tokenFallback(address,uint256,bytes)";

    constructor (string memory _name, string memory _symbol) public {
        name = _name;
        symbol = _symbol;
        decimals = 18;
    }

    function balanceOf(address account) public view override returns (uint) {
        return _balances[account];
    }

    function transfer(address to, uint value) public override returns (bool) {
        return _transfer(msg.sender, to, value, "", _tokenFallback);
    }

    function transfer(address to, uint value, bytes memory data) public override returns (bool) {
        return _transfer(msg.sender, to, value, data, _tokenFallback);
    }

    function transfer(address to, uint value, bytes memory data, string memory customFallback) public override returns (bool) {
        return _transfer(msg.sender, to, value, data, customFallback);
    }

    /* Helper functions */
    function _transfer(address from, address to, uint value, bytes memory data, string memory customFallback) internal returns (bool) {
        require(from != address(0), "ERC223: transfer from the zero address");
        require(to != address(0), "ERC223: transfer to the zero address");
        require(_balances[from] >= value, "ERC223: transfer amount exceeds balance");
        _balances[from] -= value;
        _balances[to] += value;

        if (_isContract(to)) {
            (bool success,) = to.call{value: 0}(
                abi.encodeWithSignature(customFallback, msg.sender, value, data)
            );
            assert(success);
        }
        emit Transfer(msg.sender, to, value, data);
        return true;
    }

    function _mint(address to, uint value) internal {
        require(to != address(0), "ERC223: mint to the zero address");
        totalSupply += value;
        _balances[to] += value;
        emit Transfer(address(0), to, value, "");
    }

    function _isContract(address addr) internal view returns (bool) {
        uint length;
        assembly {
            length := extcodesize(addr)
        }
        return (length > 0);
    }
}

contract Election is ERC223 {
    struct Proposal {
        string name;
        string policies;
        bool valid;
    }
    struct Ballot {
        address candidate;
        uint votes;
    }

    uint randomNumber = 0;
    bool public sendFlag = false;   //6
    address public owner;           //6
    uint public stage;              //7 
    address[] public candidates;    //8
    bytes32[] public voteHashes;    //9
    mapping(address => Proposal) public proposals;    //10
    mapping(address => uint) public voteCount;       //11
    mapping(address => bool) public voted;
    mapping(address => bool) public revealed;

    event Propose(address, Proposal);
    event Vote(bytes32);
    event Reveal(uint, Ballot[]);
    event SendFlag(address);

    constructor() public ERC223("Election", "ELC") {
        owner = msg.sender;
        _setup();
    }

    modifier auth {
        require(msg.sender == address(this) || msg.sender == owner, "Election: not authorized");
        _;
    }

    function propose(address candidate, Proposal memory proposal) public auth returns (uint) {
        require(stage == 0, "Election: stage incorrect");
        require(!proposals[candidate].valid, "Election: candidate already proposed");
        candidates.push(candidate);
        proposals[candidate] = proposal;
        emit Propose(candidate, proposal);
        return candidates.length - 1;
    }

    function vote(bytes32 voteHash) public returns (uint) {
        require(stage == 1, "Election: stage incorrect");
        require(!voted[msg.sender], "Election: already voted");
        voted[msg.sender] = true;
        voteHashes.push(voteHash);
        emit Vote(voteHash);
        return voteHashes.length - 1;
    }

    function reveal(uint voteHashID, Ballot[] memory ballots) public {
        require(stage == 2, "Election: stage incorrect");
        require(!revealed[msg.sender], "Election: already revealed");
        require(voteHashes[voteHashID] == keccak256(abi.encode(ballots)), "Election: hash incorrect");
        revealed[msg.sender] = true;

        uint totalVotes = 0;
        for (uint i = 0; i < ballots.length; i++) {
            address candidate = ballots[i].candidate;
            uint votes = ballots[i].votes;
            totalVotes += votes;
            voteCount[candidate] += votes;
        }
        require(totalVotes <= balanceOf(msg.sender), "Election: insufficient tokens");
        emit Reveal(voteHashID, ballots);
    }

    function getWinner() public view returns (address) {
        require(stage == 3, "Election: stage incorrect");
        uint maxVotes = 0;
        address winner = address(0);
        for (uint i = 0; i < candidates.length; i++) {
            if (voteCount[candidates[i]] > maxVotes) {
                maxVotes = voteCount[candidates[i]];
                winner = candidates[i];
            }
        }
        return winner;
    }

    function giveMeMoney() public {
        require(balanceOf(msg.sender) == 0, "Election: you're too greedy");
        _mint(msg.sender, 1);
    }

    function giveMeFlag() public {
        require(msg.sender == getWinner(), "Election: you're not the winner");
        require(proposals[msg.sender].valid, "Election: no proposal from candidate");
        if (_stringCompare(proposals[msg.sender].policies, "Give me the flag, please")) {
            sendFlag = true;
            emit SendFlag(msg.sender);
        }
    }

    /* Helper functions */
    function _setup() public auth {
        address Alice = address(0x9453);
        address Bob = address(0x9487);
        _setStage(0);
        propose(Alice, Proposal("Alice", "This is Alice", true));
        propose(Bob, Proposal("Bob", "This is Bob", true));
        voteCount[Alice] = uint(-0x9453);
        voteCount[Bob] = uint(-0x9487);
        _setStage(1);
    }

    function _setStage(uint _stage) public auth {
        stage = _stage & 0xff;
    }

    function _stringCompare(string memory a, string memory b) internal pure returns (bool) {
        return keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b));
    }
    
    /* custom added functions */
    function testdeet(address to, uint value, bytes memory data, string memory customFallback) pure public returns (bytes memory){
        return abi.encodeWithSignature(customFallback, to, value, data);
    }

    function properEncode(address candidate, Proposal memory proposal, address t1, address t2) pure public {

    }

    function ballotEncode(Ballot[] memory ballots) pure public returns (bytes32){
    return keccak256(abi.encode(ballots));
    }
}
