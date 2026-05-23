css_content = """
.kitchen {
    height: 100vh;
    overflow: hidden;
}

.kitchen .body_wrapper {
    position: relative;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    background-color: #878d97;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.kitchen .top_bar {
    background-color: #ffffff;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px;
    height: 56px;
    flex-shrink: 0;
}

.kitchen .top_bar .left_section,
.kitchen .top_bar .right_section {
    display: flex;
    align-items: center;
    gap: 15px;
}

.kitchen .top_bar .center_filters {
    display: flex;
    gap: 10px;
    height: 100%;
    align-items: center;
}

.kitchen .filter-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    color: #495057;
    text-decoration: none;
    font-weight: 500;
    font-size: 15px;
    border-radius: 4px;
    transition: background-color 0.2s;
    cursor: pointer;
}

.kitchen .filter-btn:hover {
    background-color: #e9ecef;
}

.kitchen .filter-btn.active {
    background-color: #ced4da;
    color: #212529;
}

.kitchen .badge-count {
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 700;
    color: white;
}

.kitchen .badge-grey { background-color: #6c757d; }
.kitchen .badge-blue { background-color: #0d6efd; }
.kitchen .badge-green { background-color: #198754; }

.kitchen .action-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #495057;
    font-weight: 500;
    font-size: 15px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 6px 10px;
}

.kitchen .action-btn:hover {
    color: #212529;
}

.kitchen .action-btn i {
    font-size: 16px;
}

.kitchen .orders_container {
    padding: 20px;
    overflow-y: auto;
    flex-grow: 1;
}

.kitchen .card {
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    background: #ffffff;
    border: none;
    transition: transform 0.2s;
}

.kitchen .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.kitchen .card-header {
    border-bottom: 1px solid #f0f0f0;
}

.kitchen .bg_grey { background-color: #6c757d !important; }
.kitchen .bg_blue { background-color: #0d6efd !important; }
.kitchen .bg_green { background-color: #198754 !important; }

.kitchen .accept_order_line:hover {
    background-color: #f8f9fa;
}
"""

with open('custom_addons/pos_kitchen_screen_odoo/static/src/css/kitchen_screen.css', 'w') as f:
    f.write(css_content)

print("CSS rewritten.")
