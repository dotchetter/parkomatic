using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System;
using Microsoft.Azure.Devices;
using System.Threading.Tasks;

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
        static ServiceClient serviceClient;
        static string connectionString = Environment.GetEnvironmentVariable("iotHubConnectionString");

        [FunctionName("DeviceMessageHandler")]
        public static void Run([IoTHubTrigger("messages/events", Connection = "ConnectionString")] EventData message, ILogger log)
        {
            log.LogInformation($"C# IoT Hub trigger function processed a message: {Encoding.UTF8.GetString(message.Body.Array)}");
            DeviceMessage deviceMessage = JsonConvert.DeserializeObject<DeviceMessage>(Encoding.UTF8.GetString(message.Body.Array));
            serviceClient = ServiceClient.CreateFromConnectionString(connectionString);
            SendCloudToDeviceMessageAsync(deviceMessage.deviceId).Wait();
        }

        private async static Task SendCloudToDeviceMessageAsync(string deviceId)
        {
            var commandMessage = new Message(Encoding.ASCII.GetBytes(DateTime.Now.ToString("HH:mm")));
            await serviceClient.SendAsync(deviceId, commandMessage);
        }
    }
}
