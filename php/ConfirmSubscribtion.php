Yehaaa.. you succesfully subscribed to our e-mail newsletter!
<?php

function update_subscribtion_confirmed($subscribeID_p) {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'ConfirmSubscribtionUser', '<PUT_YOUR_CONFIRM_SUBSCRIBTION_USER_PASSWORD_HERE>');

	// prepare and execute insert
  $sql_l = "UPDATE subscriber SET subscribtionConfirmed=true WHERE subscribeID=?";
  $pdo_l->prepare($sql_l)->execute([$subscribeID_p]);

	//echo "Updated newsletter subscribtion with subscribeID " . $subscribeID_p . "<br />";
}

// main
if ($_GET["data"] != "") {
	$subscribtionID = $_GET["data"];
  //echo "ID is " . $subscribtionID . "<br />";
	update_subscribtion_confirmed($subscribtionID);
}


?>
