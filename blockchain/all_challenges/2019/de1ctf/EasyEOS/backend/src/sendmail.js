'use strict';
const nodemailer = require('nodemailer');

function sendmail(address) {

    // create reusable transporter object using the default SMTP transport
    let transporter = nodemailer.createTransport({
        service:'126',
        port: 465,
        secure: true, // true for 465, false for other ports
        auth: {
            user: 'xxxxxx@xxxx.com', // generated ethereal user
            pass: 'xxxxxxxxxxxxxxxx'  // generated ethereal password
        }
    });

    // setup email data with unicode symbols
    let mailOptions = {
        from: '"De1ctf" <xxxxxx@xxxx.com>', // sender address
        to: address, // list of receivers
        subject: 'Flag', // Subject line
        text: 'de1ctf{h3ll0_w0r1d_e0s}', // plain text body
        html: '<b>de1ctf{h3ll0_w0r1d_e0s}</b>' // html body
    };

    // send mail with defined transport object
    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            return console.log(error);
        }
        console.log('Message sent: %s', info.messageId);
        // Preview only available when sending through an Ethereal account
        console.log('Preview URL: %s', nodemailer.getTestMessageUrl(info));

        // Message sent: <b658f8ca-6296-ccf4-8306-87d57a0b4321@blurdybloop.com>
        // Preview URL: https://ethereal.email/message/WaQKMgKddxQDoou...
    });
}


module.exports=sendmail;
