// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract GMRSmartContract {
    struct Booking {
        uint256 startTime;
        uint256 endTime;
        address customer;
        string machine;
        bool isbooked;
    }

    Booking[] public bookings;
    string[] public machines;
    uint256 slotPrice = 50;
    address public owner;

    constructor() public {
        owner = msg.sender;
        machines.push("A");
        machines.push("B");
        machines.push("C");
        machines.push("D");
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function book(
        string memory _machine_name,
        uint256 _start_time,
        uint256 _end_time
    ) public payable {
        require(msg.value >= slotPrice);
        require(checkTime(_start_time, _end_time));
        require(checkSlot(_machine_name, _start_time, _end_time));
        require(checkMachine(_machine_name));
        bookings.push(
            Booking(_start_time, _end_time, msg.sender, _machine_name, true)
        );
    }

    function checkSlot(
        string memory _machine_name,
        uint256 _start_time,
        uint256 _end_time
    ) public view returns (bool) {
        bool slot_free = true;
        for (uint256 i = 0; i < bookings.length; i++) {
            if (
                (keccak256(bytes(bookings[i].machine)) ==
                    keccak256(bytes(_machine_name))) &&
                (bookings[i].startTime <= _start_time) &&
                (bookings[i].endTime > _start_time)
            ) {
                slot_free = false;
            } else if (
                (keccak256(bytes(bookings[i].machine)) ==
                    keccak256(bytes(_machine_name))) &&
                (bookings[i].startTime < _end_time) &&
                (bookings[i].endTime > _end_time)
            ) {
                slot_free = false;
            }
        }
        return slot_free;
    }

    function checkMachine(string memory _machine_name)
        public
        view
        returns (bool)
    {
        bool machine_exists = false;
        for (uint256 i = 0; i < machines.length; i++) {
            if (
                keccak256(bytes(machines[i])) == keccak256(bytes(_machine_name))
            ) {
                machine_exists = true;
                break;
            }
        }
        return machine_exists;
    }

    function checkAccess(string memory _machine_name, uint256 _time)
        public
        view
        returns (bool)
    {
        bool access_exists = true;
        for (uint256 i = 0; i < bookings.length; i++) {
            if (
                (keccak256(bytes(bookings[i].machine)) ==
                    keccak256(bytes(_machine_name))) &&
                (bookings[i].startTime <= _time) &&
                (bookings[i].endTime > _time)
            ) {
                access_exists = false;
            }
        }
        return access_exists;
    }

    function checkTime(uint256 _start_time, uint256 _end_time)
        internal
        pure
        returns (bool)
    {
        bool valid_time = false;
        if ((_start_time > 0) && (_start_time < 2400)) {
            valid_time = true;
        }
        if ((_end_time > 0) && (_end_time < 2400)) {
            valid_time = true;
        }
        if (_start_time - (_start_time % 100) < 60) {
            valid_time = true;
        }
        if (_end_time - (_end_time % 100) < 60) {
            valid_time = true;
        }
        if (_start_time % 100 == _end_time % 100) {
            if (_end_time - _start_time == 30) {
                valid_time = true;
            }
        } else if ((_end_time % 100) - (_start_time % 100) == 1) {
            if (_end_time - _start_time - 40 == 30) {
                valid_time = true;
            }
        }
        return valid_time;
    }

    function addMachine(string memory _machine_name) public onlyOwner {
        machines.push(_machine_name);
    }

    function setSlotPrice(uint256 _slot_price) public onlyOwner {
        slotPrice = _slot_price;
    }

    function withdraw(address _recipient) public payable onlyOwner {
        payable(_recipient).transfer(address(this).balance);
    }
}
