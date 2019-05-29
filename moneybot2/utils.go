package moneybot2

import (
	"time"

	"github.com/sirupsen/logrus"

	tb "gopkg.in/tucnak/telebot.v2"
)

// Timestamp returns unix now time
func Timestamp() int32 {
	return int32(time.Now().UnixNano()) / int32(time.Second)
}

func GetLocalTime(timestamp int32) time.Time {
	unixTime := time.Unix(int64(timestamp), 0)
	t, err := time.LoadLocation("Europe/Kiev")
	if err != nil {
		logrus.Panic(err)
	}
	return unixTime.In(t)
}

// DeleteSystemMessage tries to delete sent message
func DeleteSystemMessage(m *tb.Message, b *tb.Bot, timeout time.Duration) {
	time.Sleep(timeout)
	err := b.Delete(m)
	if err != nil {
		logrus.Info(err)
	}
	logrus.Info("Remove service message ", m.ID)
}

// SendServiceMessage tries to sent message
func SendServiceMessage(to tb.Recipient, b *tb.Bot, text string, displayTimeout time.Duration) error {
	serviceMessage, err := b.Send(to, text, tb.ModeMarkdown, tb.Silent)
	if err != nil {
		return err
	}
	logrus.Infof("Send service message %v with text: %s", serviceMessage.ID, serviceMessage.Text)
	go DeleteSystemMessage(serviceMessage, b, displayTimeout)

	return nil
}