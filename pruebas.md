# Resumen de Pruebas en la Aplicación

| **Clase de Prueba**             | **Método**                               | **Descripción**                                                                                  |
|----------------------------------|------------------------------------------|--------------------------------------------------------------------------------------------------|
| **CartTest**                     | setUp                                    | Crea una categoría y un producto de prueba, y simula una sesión de usuario.                    |
|                                  | test_cart_initialization                 | Verifica que el carrito esté vacío al inicializarse.                                          |
|                                  | test_add_product                         | Agrega un producto al carrito y verifica que se haya añadido correctamente.                     |
|                                  | test_add_product_quantity                | Agrega el mismo producto con una cantidad diferente y verifica que la cantidad se actualice.    |
|                                  | test_session_modified                    | Comprueba que la sesión se marque como modificada al agregar un producto.                       |
|                                  | test_delete_product                      | Verifica que el producto se elimine del carrito correctamente.                                  |
|                                  | test_update_product                      | Actualiza la cantidad de un producto y verifica que la nueva cantidad se refleje.              |
| **CartAddViewTest**             | setUp                                    | Crea una categoría y un producto de prueba.                                                    |
|                                  | test_cart_add_post                      | Verifica que se pueda agregar un producto al carrito mediante una solicitud POST.               |
|                                  | test_cart_add_invalid_product_id        | Comprueba que se retorne un error 404 al intentar agregar un producto con un ID inválido.      |
|                                  | test_cart_add_invalid_quantity           | Verifica que se retorne un error 400 al enviar una cantidad no válida.                          |
|                                  | test_cart_add_method_not_allowed        | Comprueba que se retorne un error 405 al usar el método GET en lugar de POST.                  |
| **CategoryModelTest**           | setUp                                    | Crea una categoría de prueba.                                                                   |
|                                  | test_str_method                         | Verifica que el método `__str__` retorne el nombre correcto de la categoría.                   |
|                                  | test_get_absolute_url                   | Comprueba que se retorne la URL absoluta correcta de la categoría.                              |
| **ProductModelTest**            | setUp                                    | Crea una categoría y un producto de prueba.                                                    |
|                                  | test_str_method                         | Verifica que el método `__str__` retorne el nombre correcto del producto.                      |
|                                  | test_get_absolute_url                   | Comprueba que se retorne la URL absoluta correcta del producto.                                 |
| **StoreViewTest**               | setUp                                    | Crea una categoría y un producto de prueba.                                                    |
|                                  | test_store_view                         | Verifica que la vista de la tienda cargue correctamente y contenga el producto esperado.       |
| **CategoriesViewTest**          | setUp                                    | Crea una categoría de prueba.                                                                   |
|                                  | test_categories_view                    | Comprueba que la categoría esté correctamente creada.                                          |
| **ListCategoryViewTest**        | setUp                                    | Crea una categoría y dos productos de prueba.                                                  |
|                                  | test_list_category_view                 | Verifica que la vista de lista de categorías cargue correctamente y contenga los productos.     |
| **ProductInfoViewTest**         | setUp                                    | Crea una categoría y un producto de prueba.                                                    |
|                                  | test_product_info_view                  | Verifica que la vista de información del producto cargue correctamente y contenga la información. |
