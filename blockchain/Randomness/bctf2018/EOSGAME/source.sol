contract EOSToken{
    using SafeMath for uint256;
    string TokenName = "EOS";
    uint256 totalSupply = 100**18;
    address owner;
    mapping(address => uint256)  balances;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    constructor() public{
        owner = msg.sender;
        balances[owner] = totalSupply;
    }
    function mint(address _to,uint256 _amount) public onlyOwner {
        require(_amount < totalSupply);
        totalSupply = totalSupply.sub(_amount);
        balances[_to] = balances[_to].add(_amount);
    }
    function transfer(address _from, address _to, uint256 _amount) public onlyOwner {
        require(_amount < balances[_from]);
        balances[_from] = balances[_from].sub(_amount);
        balances[_to] = balances[_to].add(_amount);
    }
    function eosOf(address _who) public constant returns(uint256){
        return balances[_who];
    }
}

contract EOSGame{
    using SafeMath for uint256;
    mapping(address => uint256) public bet_count;
    uint256 FUND = 100;
    uint256 MOD_NUM = 20;
    uint256 POWER = 100;
    uint256 SMALL_CHIP = 1;
    uint256 BIG_CHIP = 20;
    EOSToken  eos;

    event FLAG(string b64email, string slogan);

    constructor() public{
        eos=new EOSToken();
    }
    function initFund() public{
        if(bet_count[tx.origin] == 0){
            bet_count[tx.origin] = 1;
            eos.mint(tx.origin, FUND);
        }
    }
    function bet(uint256 chip) internal {
        bet_count[tx.origin] = bet_count[tx.origin].add(1);
        uint256 seed = uint256(keccak256(abi.encodePacked(block.number)))+uint256(keccak256(abi.encodePacked(block.timestamp)));
        uint256 seed_hash = uint256(keccak256(abi.encodePacked(seed)));
        uint256 shark = seed_hash % MOD_NUM;
        uint256 lucky_hash = uint256(keccak256(abi.encodePacked(bet_count[tx.origin])));
        uint256 lucky = lucky_hash % MOD_NUM;
        if (shark == lucky){
            eos.transfer(address(this), tx.origin, chip.mul(POWER));
        }
    }
    function smallBlind() public {
        eos.transfer(tx.origin, address(this), SMALL_CHIP);
        bet(SMALL_CHIP);
    }
    function bigBlind() public {
        eos.transfer(tx.origin, address(this), BIG_CHIP);
        bet(BIG_CHIP);
    }
    function eosBlanceOf() public view returns(uint256) {
        return eos.eosOf(tx.origin);
    }
    function CaptureTheFlag(string b64email) public{
        require (eos.eosOf(tx.origin) > 18888);
        emit FLAG(b64email, "Congratulations to capture the flag!");
    }
}
