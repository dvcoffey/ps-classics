## Testing

### Navigation Testing
 
#### Navigation bar

The brand/Logo will return the user to the homepage
- success

The 'Home' link will return the user to the homepage
- success

The 'Game' link will direct the usser to the game repository
- success

The 'Log In' link will direct the user to the log in page
- success

The 'Register' link will direct the user to the registration page
- success

The 'Profile' link will direct the user to the profile page
- success

The 'Add Game' link will direct the user to the Add Game page
- success

The 'Manage Genres' link will direct the user to the genre manager page
- success

The 'Log Out' link will redirect the user to the Log In page
- success

#### Homepage

The 'Most recent' game thumbnails will direct the user to the associated game details page
- success

The 'Most viewed' game thumbnails will direct the user to the associated game details page
- success

The genre cards will direct the user to the game directory
- success

#### Game Directory

The game cards will direct the user the the game details page of the associated game
- success

The 'Search on Amazon' Button will open amazon in a new window with the search results for the associated game
- success

#### log in

A successful login will direct the user to thir profile page
- success

The 'Register Account' link will direct the user to the registration page
- success

#### Register

A successful registration will direct the user to their profile page
-success

The 'Log In' link will direct the user to the Log In page
- success

#### Profile

The game card image or title will direct the user to the associated game's details page
- success

#### Add Game

A succesful add game will redirect the user to the game database page 
- success

#### Manage Genre

The Add Genre button will direct the user to the add genre page
- success

The Edit Genre button will direct the user to the edit genre page
- success

#### Game details

The 'Search on Amazon' Button will open amazon in a new window with the search results for the associated game
-success

The Edit Game button will direct the user to the edit game page
- success

#### Edit game

A succesfully added game will keep the user on the edit game page
- success

The cancel button will return the user to the game directory page
- success

#### Edit Genre

Submit button will return user to the manage genres page
- success

Cancel button will return user to the manage genres page
- success

### Modals

#### Delete Game

On the game details page the delete button will make a confirmation modal appear
- success

The cancel button will close the modal
- success

The Modal delete button will return the user to the game directory page
- success

#### Delete Genre

On the manage genres page the delete button will make a confirmation modal appear
- success

The cancel button will close the modal
- success

The Modal delete button will return the user to the manage genres page
- success

#### 404

A 404 error will direct the user to the 404 page
- success

The back to home button will return the user to the homepage
- success

#### Footer

Youtube link opens Youtube in new window
-success

Facebook link opens facebook in new window
-success

Twitter link opens Twitter in new window
-success

### Functionality Testing

#### Registration

If username already exists, flash message user already exists
- success

#### login

If user inputs incorrect username/password, flash message incorrect username/password
- success

#### Homepage

Most recent games show the most recently added games to the database
- success

Most viewed games show the most viewed games in the database
- success

Genre cards will filter the games shown by genre
- success

#### Game Directory

Search bar returns results that match the query
- success

The reset button clears the search bar
- success

#### Profile

The profile page only shows the games added by the profile owner
- success

#### Add Game

The add game inputs the data to the correct game fields
- success

A null value or a broken image URL will display the default image "playstation logo" for the associated game
- success

The calender picker and dropdown selector are working correctly
- success

The added game will appear in the database correctly
- success

#### Edit Game

The edited game inputs the data to the correct game fields
- success

A null value or a broken image URL will display the default image "playstation logo" for the associated game
- success

The calender picker and dropdown selector are working correctly
- success

The edited game will appear in the database correctly
- success

#### Delete Game

A deleted game will be removed from the database
- success

#### Manage genres

The add, edit and delete functionality if the genres are working correctly
- success

#### Navbar
The navbar will display the appropriate links determined by the user (Visitor, Logged in or Administrator)
- success

## Responsiveness

The grids on the homepage will display as follows
- 4 for a large screen
- 2 for a medium screen
- 1 for a small screen

The grids on the game directory page will display as follows
- 3 for a large screen
- 2 for a medium screen
- 1 for a small screen

This works well, I have yet to find a game title that causes overflow
'Castlevania, Symphony of the Night' caused this issue early in development, and so the game cards were given more space to accomodate lengthier information.
The Genre cards on the homepage were initially set to 2 per row across on small screens. This caused overflow and was later to 1 per row.

The mobile sidenav is working correctly.

The site will appear correctly down to a screen width of 300px


## Validation


### HTML

The html was validated here at https://validator.w3.org/ with one error

    Warning: Section lacks heading. Consider using h2-h6 elements to add identifying headings to all sections.

    From line 50, column 5; to line 50, column 13

This is caused by the jinja tmplates used across the site.


### CSS

The CSS was validated here at https://jigsaw.w3.org/css-validator/ with one error

    URI : https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css
    13 	.table-of-contents a 	Value Error : letter-spacing only 0 can be a unit. You must put a unit after your number : 0.4 

This appears to be an artefact cause by the MaterializeCSS library as it does not target my own CSS


### Javascript

Javascript was validated at https://beautifytools.com/javascript-validator.php with 2 errors

    24	9	'let' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).
    25	9	'let' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).

### Python

Python was validated at https://extendsclass.com/python-tester.html with no errors detected.


### Further Testing

A link to the site was provided to two other people who were able to use the site without any issues.