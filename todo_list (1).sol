// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.5.0 <0.9.0;

contract TodoList{
    uint public taskCount = 0;

    struct Task{
        uint id;
        string content;
        bool completed;
    }

    mapping(uint => Task) public tasks;

    constructor() {
        createTask("This is the first task!");
    }

    function createTask(string memory _content) public {
        taskCount++;
        tasks[taskCount] = Task(taskCount,_content,false);

    }

    function toggleCompleted(uint _id) public returns(bool _bool){
        Task memory _task = tasks[_id];
        _task.completed = !_task.completed;
        tasks[_id] = _task;
        return true;


    }

    function getTask(uint _id) public view returns(uint _Id, string memory _content, bool _completed){
        Task memory _task = tasks[_id];
        return (_task.id, _task.content,_task.completed);
    }

}
