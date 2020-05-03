<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Yehaaa.. you succesfully subscribed to our e-mail newsletter!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        color: #153643;
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 20px;
    </style>
</head>

<body style="margin: 0; padding: 0;" bgcolor="#F4F4F4">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="60%" style="border-collapse: collapse; box-shadow: 0px 0px 36px 15px rgba(0, 0, 0, 0.28);">
        <tr>
            <td style="padding-top: 10px; padding-right: 10px; padding-bottom: 8px; padding-left: 5px;">
                <img src="https://stormy-stories.surf/data/stormy-stories-newsletter-mails/mails/subscribtion/logo.png" alt="You should see our logo here, but this was blocked by your mail-client" class="center" style="width: 50%;" />
            </td>
        </tr>
        <tr>
            <tr>
                <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 24px; text-align: center;" bgcolor="#323846">
                    <b>Yehaaa.. you succesfully subscribed to our e-mail newsletter!</b>
                </td>
            </tr>
            <tr>
                <td bgcolor="#f4f4f4" style="padding-top: 10px; padding-right: 10px; padding-bottom: 8px; padding-left: 5px;">
                    <p><br/></p>
                    <p>You now successfully subscribed to our e-mail newsletter!</p>
                    <p>You will from now on automatically receive a mail, when we publish a new post.</p>
                    <p>Click <a href="https://stormy-stories.surf" style="color: #000000;"><font color="#000000">here<font/></a> to directly start reading!</p>
                    <p><br/></p>
                    <p>Thanks a lot for your interest!</p>
										<p>Your stormy-stories team!</p>
                    <p><br/></p>
                    <hr style: dashed>
                    <p><br/></p>
                    <p>Du hast dich erfolgreich für unseren E-Mail Newsletter angemeldet!</p>
                    <p>Ab sofort wirst du automatisch per Mail über unsere neuen Beiträge benachrichtigt.</p>
                    <p>Klicke <a href="https://stormy-stories.surf" style="color: #000000;"><font color="#000000">hier<font/></a> um direkt zu unserem Blog zu kommen!</p>
                    <p><br/></p>
                    <p>Vielen Dank für dein Interesse!</p>
										<p>Dein stormy-stories Team!</p>
                    <p><br/></p>
                </td>
            </tr>
            <tr bgcolor="#323846">
                <td style="padding: 2px 2px 2px 2px;">

                </td>
            </tr>
            <tr>
                <td bgcolor="#323846" style="padding-top: 10px; padding-right: 10px; padding-bottom: 8px; padding-left: 5px;">
                    <table width="100%" border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="30%">
                                &reg; stormy-stories.surf 2020
                                <br/>
                            </td>
                            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" align="right" width="70%">
                                <font color="#ffffff"><a href="https://stormy-stories.surf/impressum/" align="right" style="color: #ffffff;">Impressum</a><font/>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
    </table>

<?php

function update_subscribtion_confirmed($subscribeID_p) {
        // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'ConfirmSubscribtionUser', 'TfLtK36uNteCBGhR8Bx9CNfP6tgNw6DXpy3vfVDJSXmyGvuxBLQNivCXP8cb4S8f');

	// prepare and execute update
  $sql_l = "UPDATE subscriber SET subscribtionConfirmed=true WHERE subscribeID=?";
  $pdo_l->prepare($sql_l)->execute([$subscribeID_p]);

	//echo "Updated newsletter subscribtion with subscribeID " . $subscribeID_p . "<br />";
}

// main
if ($_GET["data"] != "") {
	$subscribeID = $_GET["data"];
  //echo "ID is " . $subscribeID . "<br />";
	update_subscribtion_confirmed($subscribeID);
}


?>
</html>
