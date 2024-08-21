pragma solidity ^0.8.0;

contract AdminManagement {
    struct Directory {
        string createdAt;
    }

    struct User {
        mapping(string => Directory) directories;
        string directoryAccessible;-
        string directoryDesignation;
        string email;
        string ip;
        string name;
        string phone;
        string role;
    }

    struct Project {
        mapping(string => User) users;
    }

    struct Admin {
        string email;
        string name;
        string phone;
        mapping(string => Project) projects;
        string role;
    }

    mapping(string => Admin) public admins;

    // Function to add or update an admin
    function setAdmin(
        string memory adminId,
        string memory email,
        string memory name,
        string memory phone,
        string memory role
    ) public {
        Admin storage admin = admins[adminId];
        admin.email = email;
        admin.name = name;
        admin.phone = phone;
        admin.role = role;
    }

    // Function to add or update a project for an admin
    function setProject(
        string memory adminId,
        string memory projectId
    ) public {
        Admin storage admin = admins[adminId];
        Project storage project = admin.projects[projectId];
    }

    // Function to add or update a user for a project
    function setUser(
        string memory adminId,
        string memory projectId,
        string memory userId,
        string memory directoryAccessible,
        string memory directoryDesignation,
        string memory email,
        string memory ip,
        string memory name,
        string memory phone,
        string memory role
    ) public {
        Admin storage admin = admins[adminId];
        Project storage project = admin.projects[projectId];
        User storage user = project.users[userId];
        user.directoryAccessible = directoryAccessible;
        user.directoryDesignation = directoryDesignation;
        user.email = email;
        user.ip = ip;
        user.name = name;
        user.phone = phone;
        user.role = role;
    }

    // Function to add or update a directory for a user
    function setDirectory(
        string memory adminId,
        string memory projectId,
        string memory userId,
        string memory directoryId,
        string memory createdAt
    ) public {
        Admin storage admin = admins[adminId];
        Project storage project = admin.projects[projectId];
        User storage user = project.users[userId];
        Directory storage directory = user.directories[directoryId];
        directory.createdAt = createdAt;
    }
}
