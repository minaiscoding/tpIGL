import requests

# Define the API endpoint
ENDPOINT = "http://localhost:8000/api/moderateurs/"

# Test to check if the moderators endpoint returns a 200 status code
def test_moderators_endpoint():
    """
    Test the moderators API endpoint for a successful response (status code 200).

    :return: None
    :rtype: None
    :noindex:
    """
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

# Test to add a moderator and check if it exists in the list
def test_moderateurs_add():
    """
    Test adding a moderator to the API and checking if it exists in the list.

    :return: None
    :rtype: None
    :noindex:
    """
    # Create a sample data for the moderator
    moderator_data = {
        'NomUtilisateur': 'manel',
        'Email': 'manel@example.com',
        'MotDePasse': 'password123',
        'Role': 'moderator',
    }
    
    # Send a POST request to add the moderator
    response_add = requests.post(ENDPOINT + "add", json=moderator_data)
    assert response_add.status_code == 200
    
    # Send a GET request to retrieve the list of moderators
    response_get = requests.get(ENDPOINT)
    moderateurs = response_get.json()
    
    # Check if the added moderator exists in the list
    assert any(moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur'] for moderateur in moderateurs)

# Test to add a moderator, retrieve its ID, delete it, and check if it doesn't exist anymore
def test_moderateur_delete():
    """
    Test adding a moderator, retrieving its ID, deleting it, and checking if it no longer exists.

    :return: None
    :rtype: None
    :noindex:
    """
    # Create a sample data for the moderator
    moderator_data = {
        'NomUtilisateur': 'manel',
        'Email': 'manel@example.com',
        'MotDePasse': 'password123',
        'Role': 'moderator',
    }
    
    # Send a POST request to add the moderator
    response_add = requests.post(ENDPOINT + "add", json=moderator_data)
    assert response_add.status_code == 200
    
    # Send a GET request to retrieve the list of moderators
    response_get = requests.get(ENDPOINT)
    moderateurs = response_get.json()
    
    # Check if the added moderator exists in the list
    assert any(moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur'] for moderateur in moderateurs)
    
    # Find the added moderator in the list and retrieve its ID
    added_moderator = next((moderateur for moderateur in moderateurs if moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur']), None)
    id_moderator = added_moderator["id"]
    
    # Send a DELETE request to delete the moderator
    response_delete = requests.post(ENDPOINT + f"delete/{id_moderator}")
    assert response_delete.status_code == 200
    
    # Send a GET request to retrieve the updated list of moderators
    response_get = requests.get(ENDPOINT)
    moderateurs_after_deletion = response_get.json()
    
    # Check if the added moderator doesn't exist in the updated list
    assert not any(moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur'] for moderateur in moderateurs_after_deletion)

# Test to add a moderator, retrieve its ID, update it, and check if the updated data exists
def test_moderateur_update():
    """
    Test adding a moderator, retrieving its ID, updating it, and checking if the updated data exists.

    :return: None
    :rtype: None
    :noindex:
    """
    # Create a sample data for the moderator
    moderator_data = {
        'NomUtilisateur': 'manel',
        'Email': 'manel@example.com',
        'MotDePasse': 'password123',
        'Role': 'moderator',
    }
    
    # Send a POST request to add the moderator
    response_add = requests.post(ENDPOINT + "add", json=moderator_data)
    assert response_add.status_code == 200
    
    # Send a GET request to retrieve the list of moderators
    response_get = requests.get(ENDPOINT)
    moderateurs = response_get.json()
    
    # Check if the added moderator exists in the list
    assert any(moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur'] for moderateur in moderateurs)
    
    # Find the added moderator in the list and retrieve its ID
    added_moderator = next((moderateur for moderateur in moderateurs if moderateur['NomUtilisateur'] == moderator_data['NomUtilisateur']), None)
    id_moderator = added_moderator["id"]
    
    # Create updated data for the moderator
    updated_moderator_data = {
        'NomUtilisateur': 'manel',
        'Email': 'manel@example.com',
        'MotDePasse': 'password123',
        'Role': 'moderator',
    }
    
    # Send a POST request to update the moderator
    response_update = requests.post(ENDPOINT + f"update/{id_moderator}", json=updated_moderator_data)
    assert response_update.status_code == 200
    
    # Send a GET request to retrieve the updated list of moderators
    response_get = requests.get(ENDPOINT)
    moderateurs_after_update = response_get.json()
    
    # Check if the updated data exists in the updated list
    assert any(moderateur['NomUtilisateur'] == updated_moderator_data['NomUtilisateur'] for moderateur in moderateurs_after_update)

