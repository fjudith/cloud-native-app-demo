package system

main = allow

default allow = false

allow {
	input.method = "GET"
	input.path = [""]
}

allow {
	input.method = "POST"
	input.path = [""]
}

allow {
	input.method = "GET"
	input.path = ["metrics"]
}

allow {
	input.method = "GET"
	input.path = ["apis", "spec"]
}

allow {
	input.method = "POST"
	input.path = ["apis", "dataset", "v1"]
	has_role("manager")
}

allow {
	input.method = "GET"
	input.path = ["apis", "person", "v1", guid]
    employees[input.user]
}


allow {
	input.method = "PUT"
	input.path = ["apis", "person", "v1", guid]
	has_role("manager")
}

allow {
	input.method = "POST"
	input.path = ["apis", "person", "v1", guid]
	has_role("operator")
}

allow {
	input.method = "DELETE"
	input.path = ["apis", "person", "v1", guid]
	has_role("manager")
}

has_role(name) {
	employee := employees[input.user]
	employee.roles[name]
}

employees = {
	"alice": {"roles": {"manager", "operator"}},
	"james": {"roles": {"manager"}},
	"kelly": {"roles": {"operator"}},
}