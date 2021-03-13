pragma solidity ^0.5.11;

library Math {
    function invMod(int256 _x, int256 _pp) internal pure returns (int) {
        int u3 = _x;
        int v3 = _pp;
        int u1 = 1;
        int v1 = 0;
        int q = 0;
        while (v3 > 0){
            q = u3/v3;
            u1= v1;
            v1 = u1 - v1*q;
            u3 = v3;
            v3 = u3 - v3*q;
        }
        while (u1<0){
            u1 += _pp;
        }
        return u1;
    }
    
    function expMod(int base, int pow,int mod) internal pure returns (int res){
        res = 1;
        if(mod > 0){
            base = base % mod;
            for (; pow != 0; pow >>= 1) {
                if (pow & 1 == 1) {
                    res = (base * res) % mod;
                }
                base = (base * base) % mod;
            }
        }
        return res;
    }
    function pow_mod(int base, int pow, int mod) internal pure returns (int res) {
        if (pow >= 0) {
            return expMod(base,pow,mod);
        }
        else {
            int inv = invMod(base,mod);
            return expMod(inv,abs(pow),mod);
        }
    }
    
    function isPrime(int n) internal pure returns (bool) {
        if (n == 2 ||n == 3 || n == 5) {
            return true;
        } else if (n % 2 ==0 && n > 1 ){
            return false;
        } else {
            int d = n - 1;
            int s = 0;
            while (d & 1 != 1 && d != 0) {
                d >>= 1;
                ++s;
            }
            int a=2;
            int xPre;
            int j;
            int x = pow_mod(a, d, n);
            if (x == 1 || x == (n - 1)) {
                return true;
            } else {
                for (j = 0; j < s; ++j) {
                    xPre = x;
                    x = pow_mod(x, 2, n);
                    if (x == n-1){
                        return true;
                    }else if(x == 1){
                        return false;
                    }
                }
            }
            return false;
        }
    }
    
    function gcd(int a, int b) internal pure returns (int) {
        int t = 0;
        if (a < b) {
            t = a;
            a = b;
            b = t;
        }
        while (b != 0) {
            t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
    function abs(int num) internal pure returns (int) {
        if (num >= 0) {
            return num;
        } else {
            return (0 - num);
        }
    }
    
}

contract StArNDBOX{
    using Math for int;
    constructor()public payable{
    }
    modifier StAr() {
        require(msg.sender != tx.origin);
        _;
    }
    function StArNDBoX(address _addr) public payable{
        
        uint256 size;
        bytes memory code;
        int res;
        
        assembly{
            size := extcodesize(_addr)
            code := mload(0x40)
            mstore(0x40, add(code, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(code, size)
            extcodecopy(_addr, add(code, 0x20), 0, size)
        }
        for(uint256 i = 0; i < code.length; i++) {
            res = int(uint8(code[i]));
            require(res.isPrime() == true);
        }
        bool success;
        bytes memory _;
        (success, _) = _addr.delegatecall("");
        require(success);
    }
}
