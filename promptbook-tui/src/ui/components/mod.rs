pub mod categories;
pub mod details;
pub mod footer;
pub mod header;
pub mod modals;
pub mod prompts;

pub use categories::render_categories;
pub use details::render_details;
pub use footer::render_footer;
pub use header::render_header;
pub use modals::*;
pub use prompts::render_prompts;
