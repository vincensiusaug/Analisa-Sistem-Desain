<!DOCTYPE html>
<html>
<body>
    <?php
        $dir = 'sqlite:/[YOUR-PATH]/combadd.sqlite';
        $dbh  = new PDO($dir) or die("cannot open the database");
        if($dbh){
            $query =  "SELECT * FROM combo_calcs WHERE options='easy'";
            foreach ($dbh->query($query) as $row)
            {
                echo $row[0];
            }
            $dbh = null;
        }
        else{
            echo "Opened database not successfully\n";
        }
    ?>

<!-- <?php
$color = "red";
echo "My car is " . $color . "<br>";
echo "My house is " . $COLOR . "<br>";
echo "My boat is " . $coLOR . "<br>";
?> -->

</body>
</html>





<!-- <html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
        <?php echo '<p>Hello World</p>'; ?> 

 </body>
</html> -->
