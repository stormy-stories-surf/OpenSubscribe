<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>You now successfully removed yourself from our e-mail newsletter! Sorry to see you go!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        /* Smartphones (portrait) ----------- */
        @media only screen and (max-width : 600px) {
          .responsive {
              width: 100%
          }
        }

        /* NOT Smartphones (portrait) ----------- */
        @media only screen and (min-width : 600px) {
          .responsive {
              width: 60%
          }
        }

        color: #153643;
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 20px;
    </style>
</head>

<body style="margin: 0; padding: 0;" bgcolor="#F4F4F4">
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="responsive" style="border-collapse: collapse; box-shadow: 0px 0px 36px 15px rgba(0, 0, 0, 0.28);">
        <tr>
            <td style="padding-top: 10px; padding-right: 10px; padding-bottom: 8px; padding-left: 5px;">
                <img src="https://stormy-stories.surf/data/stormy-stories-newsletter-mails/mails/subscribtion/logo.png" alt="You should see our logo here, but this was blocked by your mail-client" class="center" style="width: 50%;" />
            </td>
        </tr>
        <tr>
            <tr>
                <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 24px; text-align: center;" bgcolor="#323846">
                    <b>You now successfully removed yourself from our e-mail newsletter! Sorry to see you go!</b>
                </td>
            </tr>
            <tr>
                <td bgcolor="#f4f4f4" style="padding-top: 10px; padding-right: 10px; padding-bottom: 8px; padding-left: 5px;">
                    <p><br/></p>
                    <p>You now removed yourself from the e-mail newsletter!</p>
                    <p>It was nice to have had you as a reader, but since we respect your privacy and love the concept of anonymity and the right to be forgotten, we have now irretrievably deleted your mail address from all our databases.</p>
                    <p>If you and we now leave this website, everything will be as if we had never met.</p>
                    <p>Your data will still appear in our backups for a short time, but shortly no one will remember you here either.</p>
                    <p><br/></p>
                    <p>Maybe we will meet again one day, but until then thank you very much and see you soon.</p>
										<p>Your stormy-stories team!</p>
                    <p><br/></p>
                    <hr style: dashed>
                    <p><br/></p>
                    <p>Du hast dich erfolgreich von unserem E-Mail Newsletter abgemeldet!</p>
                    <p>Es war schön dich als Leser gehabt zu haben, aber da wir deine Privatsphäre respektieren und das Konzept der Anonymität und des Rechts auf Vergessenwerden lieben, haben wir deine Mail-Adresse nun aus allen unseren Datenbanken unwiederbringlich gelöscht.</p>
                    <p>Wenn du und wir diese Website jetzt verlassen, wird alles so sein, als hätten wir uns nie getroffen.</p>
                    <p>Für eine kurze Zeit werden deine Daten noch in unseren Backups auftauchen, doch in Kürze wird sich auch hier niemand mehr an dich zurück erinnern.</p>
                    <p><br/></p>
                    <p>Vielleicht trifft man sich einmal wieder, aber bis dahin vielen Dank und bis bis bald.</p>
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

function update_unsubscribed($unsubscribeID_p) {
  // open database connection
	$pdo_l = new PDO('mysql:host=localhost;dbname=OpenSubscribe', 'UnsubscribeUser', '<PUT_YOUR_UNSUBSCRIBE_USER_PASSWORD_HERE>');

	// prepare and execute update
  $sql_l = "UPDATE subscriber SET unSubscribed=true WHERE unsubscribeID=?";
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

</html>
