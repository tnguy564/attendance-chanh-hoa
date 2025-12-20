# auth/routes.py (Add this section)

@auth_bp.route('/api/delete-teacher', methods=['DELETE'])
def api_delete_teacher():
    # Only allow DELETE method
    if request.method != 'DELETE':
        return jsonify({"success": False, "error": "Method not allowed"}), 405
        
    data = request.get_json()
    email_to_delete = data.get('email')
    
    if not email_to_delete:
        return jsonify({"success": False, "error": "Email address is required for deletion"}), 400

    db = current_app.config.get("DB")
    # The teacher collection is db.auth_teachers, as defined in your signup code
    auth_col = db.auth_teachers 
    
    # Use PyMongo's delete_one method to remove the teacher by email
    delete_result = auth_col.delete_one({'email': email_to_delete})

    if delete_result.deleted_count == 1:
        # A document was successfully deleted
        return jsonify({
            "success": True, 
            "message": f"Teacher with email '{email_to_delete}' deleted successfully."
        }), 200
    else:
        # No document matched the email filter
        return jsonify({
            "success": False, 
            "error": f"No teacher found with email '{email_to_delete}'."
        }), 404