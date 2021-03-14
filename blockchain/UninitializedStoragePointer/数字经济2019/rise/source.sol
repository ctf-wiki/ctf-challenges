pragma solidity >=0.4.2;
contract rise {
    address referee;
    uint secret;
    uint bl;
    mapping(address => uint) public balance;
    mapping(address => uint) public gift;
    address owner;
    
    struct hacker { 
        address hackeraddress;
        uint value;
    }
    
    constructor()public{
        owner = msg.sender;
        referee = msg.sender;
        balance[msg.sender]=10000000;
        bl=1;
        secret=18487187377722;
    }
    event SendFlag(string b64email);
    
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    
    modifier onlyRefer(){
        require(msg.sender == referee);
        _;
    }
    
    function payforflag(string b64email) public
    {
        require(balance[msg.sender]>1000000);
        balance[msg.sender]=0;
        bl=1;
        owner.transfer(address(this).balance);
        emit SendFlag(b64email);
    }
    
    function airdrop() public
    {
        require(gift[msg.sender]==0);
        gift[msg.sender]==1;
        balance[msg.sender]+=1;
    }
    
    function deposit() public payable
    {
        uint geteth=msg.value/1000000000000000000;
        balance[msg.sender]+=geteth;
    }
    
    function set_secret(uint target_secret) public onlyOwner
    {
        secret=target_secret;
    }
    
    function set_bl(uint target_bl) public onlyRefer
    {
        bl=target_bl;
    }
    
    function risegame(uint guessnumber) public payable
    {
        require(balance[msg.sender]>0);
        uint geteth=msg.value/1000000000000000000;
        if (guessnumber==secret)
        {
            balance[msg.sender]+=geteth*bl;
            bl=1;
        }
        else
        {
            balance[msg.sender]=0;
            bl=1;
        }
    }
    
    function transferto(address to) public
    {
        require(balance[msg.sender]>0);
        if (to !=0)
        {
            balance[to]=balance[msg.sender];
            balance[msg.sender]=0;
        }
        else
        {
            hacker storage h;
            h.hackeraddress=msg.sender;
            h.value=balance[msg.sender];
            balance[msg.sender]=0;
        }
    }
    
}
