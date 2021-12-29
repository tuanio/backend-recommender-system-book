### Hi bro 🖐 
This is backend site.

We using flask for backend processing and our database is building by sqlite.

Dưới đây là danh sách API:

1. get book
    - Mô tả: API này dùng để lấy tất cả thông tin một quyển sách
        - review, rating, author
    - URL: **/api/get-book/<int:user_id>/<int:book_id>**
    - Method: GET
2. update count of author and genre
    - Mô tả: API này dùng để đếm lên một đơn vị cho những tác giả và thể loại có trong cuốn sách tương ứng, với một user nào đó
    - URL: **/api/update-count-author-genre/<int:user_id>/<int:book_id>**
    - Method: PUT
3. get book similar
    - Mô tả: API này dùng để lấy một list những cuốn sách tương tự như cuốn sách yêu cầu
    - URL: **/api/get-book-similar/<int:book_id>**
    - Method: GET
4. get top 100 books
    - Mô tả: API này dùng để lấy top 100 cuốn sách nổi bật nhất
    - URL: **/api/get-top-100-books**
    - Method: GET
5. update user rating
    - Mô tả: API này dùng để update rating của một cuốn sách thuộc về user nào đó
    - URL: **/api/update-user-rating/<int:user_id>/<int:book_id>/<int:user_rating>**
    - Method: PUT
6. get list book rated
    - Mô tả: API này dùng để lấy một list những cuốn sách đã rate
    - URL: **/api/get-list-book-rated/<int:user_id>**
    - Method: GET
7. update favorite
    - Mô tả: API này dùng để update trạng thái yêu thích của một user đối với một cuốn sách nào đó
    - URL: **/api/update-favorite/<int:user_id>/<int:book_id>**
    - Method: PUT
8. get book favorited
    - Mô tả: API này dùng để lấy một list những cuốn sách đã yêu thích
    - URL: **/api/get-book-favorited/<int:user_id>**
    - Method: GET
9. create user
    - Mô tả: API này dùng để tạo user
    - URL: **/api/create-user**
    - Method: POST
    
    ```json
    {
    	"uid": "uid_string_from_firebase",
    	"user_name": "user_name_sample",
    	"user_email": "mail@mail.com"
    }
    ```
    
10. get all users
    - Mô tả: API này dùng để liệt kê tất cả user có trên hệ thống
    - URL: **/api/get-all-users**
    - Method: GET
11. get reading list history
    - Mô tả: API này dùng để liệt kê tất cả sách user đã xem trong quá khứ (lịch sử xem sách)
    - URL: **/api/get-reading-list-history/<int:user_id>**
    - Method: GET
12. get all authors
    - Mô tả: API này dùng để liệt kê tất cả author hiện có trên hệ thống
    - URL: **/api/get-all-authors**
    - Method: GET
13. get all genres
    - Mô tả: API này dùng để liệt kê tất cả genre trên hệ thống
    - URL: **/api/get-all-genres**
    - Method: GET
14. get list books by author and genre
    - Mô tả: API này dùng để query những sách mà có author và genre phù hợp
    - URL: **/api/get-list-books-by-author-genre/<int:author_id>/<int:genre_id>**
    - Method: GET
15. get list book recommend by author
    - Mô tả: API này dùng để lấy top 100 cuốn sách được recommend theo author (không sắp xếp)
    - URL: **/api/get-list-book-recommend-by-author/<int:user_id>**
    - Method: GET
16. get list book recommend by genre
    - Mô tả: API này dùng để lấy top 100 cuốn sách được recommend theo genre (không sắp xếp)
    - URL: **/api/get-list-book-recommend-by-genre/<int:user_id>**
    - Method: GET
17. get some book similar at all
    - Mô tả: API này dùng để lấy ngẫu nhiên 100 (hoặc ít hơn nếu số lượng sách đã đọc không đến 10 ⇒ số lượng recommend ít hơn 100) cuốn sách tương tự như những cuốn đã đọc.
    - URL: **/api/get-some-book-similar-at-all/<int:user_id>**
    - Method: GET
18. get user
    - Mô tả: API này dùng để lấy thông tin của một user khi biết user_id
    - URL: **/api/get-user/<int:user_id>**
    - Method: GET
19. get one top book
    - Mô tả: API này dùng để lấy tất cả thông tin của một quyển sách duy nhất, nhưng quyển sách này là quyển sách được click nhiều nhất
    - URL: **/api/get-one-top-book**
    - Method: GET