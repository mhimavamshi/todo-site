const HOST = "http://localhost:8000";
const PREFIX = HOST + "/api/v1";
const PROJECT_PREFIX = PREFIX + "/projects";
const TODO_PREFIX = PREFIX + "/todos";


async function delete_call(endpoint) {
    console.log(`${endpoint} is going to be called...`);
    try {
        const response = await fetch(endpoint, {
            method: "DELETE",
        });
        return response;
    } catch (error) {
        console.error(error.message);
    }
}

async function create_call(endpoint, data) {
    console.log(`${endpoint} is going to be called...`);
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",            
            },
            body: JSON.stringify(data)
        });

        if(!response.ok) {
            throw new Error(`Response status: ${response.status} and body ${response.json()}`);
        }

        return response;
    } catch (error) {
        throw error;
    }
}

async function update_call(endpoint, data) {
    console.log(`${endpoint} is going to be called...`);
    try {
        const response = await fetch(endpoint, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",            
            },
            body: JSON.stringify(data)
        });

        if(!response.ok) {
            throw new Error(`Response status: ${response.status} and body ${response.json()}`);
        }

        return response;
    } catch (error) {
        throw error;
    }
}


async function create_project(data) {
    let response = await create_call(PROJECT_PREFIX+"/create", data);
    return response.json();
}

async function update_project(data) {
    let response = await update_call(PROJECT_PREFIX+"/update", data);
    return response.json();
}

async function delete_project(project_id) {
    let response = await delete_call(`${PROJECT_PREFIX}/${project_id}`);
    return response.ok;
}

export { delete_project, create_project, update_project };