You succesfully unsubscribed from our e-mail newsletter!
<?php

function update_unsubscribed($unsubscribeID_p) {
  // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'UnsubscribeUser', '<PUT_YOUR_UNSUBSCRIBE_USER_PASSWORD_HERE>');

	// prepare and execute update
  $sql_l = "UPDATE subscriber SET mailaddress='', unSubscribed=true WHERE unsubscribeID=?";
  $pdo_l->prepare($sql_l)->execute([$unsubscribeID_p]);

	//echo "Updated newsletter subscribtion with unsubscribeID " . $unsubscribeID_p . "<br />";
}

// main
if ($_GET["data"] != "") {
	$unsubscribeID = $_GET["data"];
  //echo "ID is " . $unsubscribeID . "<br />";
	update_unsubscribed($unsubscribeID);
}


?>
