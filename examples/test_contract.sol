pragma solidity ^0.4.18;

contract Test {
    uint256 public testValue;

    function Test(uint256 _testValue){
        testValue = _testValue;
    }

    function setTestValue(uint256 _testValue) public {
        testValue = _testValue;
    }

}
