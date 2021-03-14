pragma solidity ^0.4.24;

contract hf {
    address secret;
    uint count;
    address owner;
    
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public gift;
    
    struct node {
        address nodeadress;
        uint nodenumber;
    }
    
    node public node0;
    
    event SendFlag(string b64email);
    
    constructor()public{
        owner = msg.sender;
    }
    
    function payforflag(string b64email) public {
        require(balanceOf[msg.sender] >= 100000);
        balanceOf[msg.sender]=0;
        owner.transfer(address(this).balance);
        emit SendFlag(b64email);
    }
    

    //to fuck
    
    modifier onlySecret() {
        require(msg.sender == secret);
        _;
    }
    
    function profit() public{
        require(gift[msg.sender]==0);
        gift[msg.sender]=1;
        balanceOf[msg.sender]+=1;
    }
    
    function hfvote() public payable{
        uint geteth=msg.value/1000000000000000000;
        balanceOf[msg.sender]+=geteth;
    }
    
    function ubw() public payable{
        if (msg.value < 2 ether)
        {
            node storage n = node0;
            n.nodeadress=msg.sender;
            n.nodenumber=1;
        }
        else
        {
            n.nodeadress=msg.sender;
            n.nodenumber=2;
        }
    }
    
    function fate(address to,uint value) public onlySecret {
        require(balanceOf[msg.sender]-value>=0);
        balanceOf[msg.sender]-=value;
        balanceOf[to]+=value;
    }
    
}
