using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System;

namespace DeviceMessageHandler
{

    public class DeviceMessage

    {
        public float lon { get; set; }
        public float lat { get; set; }
        public long epochtime { get; set; }
        public string deviceId { get; set; }

    }
    // "{\"lat\": \"%s\", \"lon\": \"%s\", \"deviceId\": \"%s\", \"epochtime\": %ld}"
    public static class DeviceMessageHandler
    {
        private static HttpClient client = new HttpClient();

        [FunctionName("DeviceMessageHandler")]
        public static void Run([IoTHubTrigger("messages/events", Connection = "ConnectionString")]EventData message, ILogger log)
        {
            log.LogInformation($"C# IoT Hub trigger function processed a message: {Encoding.UTF8.GetString(message.Body.Array)}");
            DeviceMessage deviceMessage = JsonConvert.DeserializeObject<DeviceMessage>(Encoding.UTF8.GetString(message.Body.Array));

            string time = DateTime.Now.ToString("HH:mm");
            log.LogInformation($"The current time: {time}");

        }

       
    }

}