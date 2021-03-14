pragma solidity >=0.4.2;
contract cow{
    address public owner_1;
    address public owner_2;
    address public owner_3;
    address public owner;
    mapping(address => uint) public balance;
    
    struct hacker { 
        address hackeraddress1;
        address hackeraddress2;
    }
    hacker  h;
    
    constructor()public{
        owner = msg.sender;
        owner_1 = msg.sender;
        owner_2 = msg.sender;
        owner_3 = msg.sender;
    }
    
    event SendFlag(string b64email);
    
    
    function payforflag(string b64email) public
    {
        require(msg.sender==owner_1);
        require(msg.sender==owner_2);
        require(msg.sender==owner_3);
        owner.transfer(address(this).balance);
        emit SendFlag(b64email);
    }
    
    function Cow() public payable
    {
        uint geteth=msg.value/1000000000000000000;
        if (geteth==1)
        {
            owner_1=msg.sender;
        }
    }
    
    function cov() public payable
    {
        uint geteth=msg.value/1000000000000000000;
        if (geteth<1)
        {
            hacker fff=h;
            fff.hackeraddress1=msg.sender;
        }
        else
        {
            fff.hackeraddress2=msg.sender;
        }
    }
    
    function see() public payable
    {
        uint geteth=msg.value/1000000000000000000;
        balance[msg.sender]+=geteth;
        if (uint(msg.sender) & 0xffff == 0x525b)
        {
            balance[msg.sender] -= 0xb1b1;
        }
    }
    
    function buy_own() public
    {
        require(balance[msg.sender]>1000000);
        balance[msg.sender]=0;
        owner_3=msg.sender;
    }
    
}
