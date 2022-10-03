#[macro_use]
extern crate rocket;

#[macro_use]
extern crate rocket_include_static_resources;

static_response_handler! {
    "/favicon.ico" => favicon => "favicon"
}

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .attach(static_resources_initializer!(
            "favicon" => "src/static/images/favicon.ico"
        ))
        .mount("/", routes![favicon])
        .mount("/", routes![index])
}