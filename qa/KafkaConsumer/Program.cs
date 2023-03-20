using System;
using System.CommandLine;
using System.CommandLine.Invocation;

using System.Runtime.CompilerServices;
using Confluent.Kafka;
using Confluent.Kafka.Admin;

// Used for reading appsettings.json
using Microsoft.Extensions.Configuration;
// NuGet packages:
// Microsoft.Extensions.Configuration.Binder
// Microsoft.Extensions.Configuration.Json

namespace kc;


/// <summary>
/// Kafka Console (kc) is a command line tool for interacting with Kafka topics.
///  Example usage: kc tail rsbc.apr.application.accepted.decoded --env test
///  
/// Example of redirecting stderr to a file and stderr to both a file and the console:
/// .\kc tail rsbc.apr.application.accepted.decoded --env test 2> stderr.log | Tee-Object -FilePath stdout.log
/// </summary>




class Program {
    static async Task<int> Main(string[] args) {
        /*
        // Create a file stream
        FileStream filestream = new FileStream("out.txt", FileMode.Create);
        // Create a stream writer
        var streamwriter = new StreamWriter(filestream);
        // Set auto flush
        streamwriter.AutoFlush = true;
        // Redirect standard error output stream
        Console.SetError(streamwriter);
        // Write some text that causes an error
        Console.Error.WriteLine("This is an error message");
        */

        // Command-line arguments supplied by System.Commandline
        // https://learn.microsoft.com/en-us/dotnet/standard/commandline/

        // The name of the Kafka topic to work on
        var topicNameArgument = new Argument<string>(
            name: "topic-name",
            description: "The name of a topic to tail.");

        // The environment to use: dev, test, or prod.
        var envOption = new Option<string?>(
            name: "--env",
            description: "The OpenShift environment to use.");

        // The root command is a command like "list, tail, help"
        var rootCommand = new RootCommand("Kafka consumer console app. For following topic messages.");

        // The list command lists all topics on a Kafka cluster
        var listCommand = new Command("list", "List Kafka topics");
        listCommand.AddOption(envOption);
        rootCommand.AddCommand(listCommand);

        // The tail command follows messages in a topic
        var tailCommand = new Command("tail", "Tail a Kafka topic");
        tailCommand.AddArgument(topicNameArgument);
        tailCommand.AddOption(envOption);
        rootCommand.AddCommand(tailCommand);

        // The list command lists all topics on a Kafka cluster
        var helpCommand = new Command("help", "Show verbose help and examples.");
        rootCommand.AddCommand(helpCommand);

        // List Kafka topics
        listCommand.SetHandler(async (env) => {
            if (env==null) {
                env="test";
            }
            await ListTopics(env);
        },
        envOption);

        // Tail Kafka topic
        tailCommand.SetHandler(async (env, topic) =>
        {
            if (env == null) {
                env = "test";
            }
            await TailTopic(env, topic);
        },
        envOption, topicNameArgument);

        // Print verbose help
        helpCommand.SetHandler(() => {
            Console.Write(GetHelpPageText());
        });

        return await rootCommand.InvokeAsync(args);
    }

    internal static async Task ListTopics(string env) {
        // Read ~/kc.json configuration file with user settings
        string configFile = "kc-" + env + ".json";
        var configuration = new ConfigurationBuilder()
          .SetBasePath(GetHomeFolder())
          .AddJsonFile(configFile, optional: false)
          .Build();
/*
        Console.WriteLine("-------------------------------------------------------------------------");
        Console.WriteLine("Config file:     " + configFile);
        Console.WriteLine("Host:            " + configuration.GetSection("Server")["bootstrap"]);
        Console.WriteLine("SSL CA location: " + configuration.GetSection("SSL")["SslCaLocation"]);
        Console.WriteLine("SSL certificate: " + configuration.GetSection("SSL")["SslCertificateLocation"]);
        Console.WriteLine("SSL key:         " + configuration.GetSection("SSL")["SslKeyLocation"]);
        //Console.WriteLine("SSL password:    " + configuration.GetSection("SSL")["SslKeyPassword"]);

        // Inspect configuration object using a breakpoint here
        Console.WriteLine("-------------------------------------------------------------------------");
*/
        try {
            /* For reference, this is my client.properties file
             * 
            # In an SSL connection, a truststore is used to store certificates from 
            # Certified Authorities (CA) that verify the certificate presented by 
            # the server, while a keystore is used to store private key and identity 
            # certificates that a specific program should present to both parties 
            # (server or client) for verification. 
            #
            # In other words, the truststore is used to verify the credentials, 
            # while the keystore is used to provide those credentials.

            security.protocol=SSL

            #Public key
            # the keystore is used to provide the credentials
            ssl.keystore.location=user.p12
            ssl.keystore.password=VCPnBUxUHU6X
            ssl.keystore.type=PKCS12

            # Private key
            # the truststore is used to verify the credentials
            # Can also be saved as a .pem/.crt with no password
            ssl.truststore.location=ca.p12
            ssl.truststore.password=MZNhFgRH3KwG
             */
            // Configuration
            // Confluent documentation:
            // https://docs.confluent.io/platform/current/clients/confluent-kafka-dotnet/_site/api/Confluent.Kafka.ConsumerConfig.html
            var kafkaConfig = new ConsumerConfig {
                BootstrapServers = configuration.GetSection("Server")["bootstrap"],
                SecurityProtocol = SecurityProtocol.Ssl,

                // CA certificates key (Path to CA certificate key, for verifying the broker's key)
                // oc --namespace=be5301-test get secret rsbc-ride-redhat-kafka-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt
                SslCaLocation = configuration.GetSection("SSL")["SslCaLocation"],

                // Public key file (Path to user certificate file)
                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.crt}' | base64 --decode > user.crt
                SslCertificateLocation = configuration.GetSection("SSL")["SslCertificateLocation"],

                // Private key file (Path to client's private key (PEM), used for authentication)
                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.key}' | base64 --decode > user.key
                SslKeyLocation = configuration.GetSection("SSL")["SslKeyLocation"],
                // Private key passphrase (for use with ssl.key.location and set_ssl_cert())

                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.password}' | base64 --decode
                SslKeyPassword = configuration.GetSection("SSL")["SslKeyPassword"],
            };

            var adminClient = new AdminClientBuilder(kafkaConfig).Build();
            var metadata = adminClient.GetMetadata(TimeSpan.FromSeconds(30));
            foreach (var topic in metadata.Topics) {
                Console.WriteLine(topic.Topic);
            }

        }
        catch (Exception ex) {
            Console.WriteLine("\n\nException: " + ex.Message);
            System.Diagnostics.Debug.WriteLine(ex.Message);
        }

    }


    internal static async Task TailTopic(string env, string topicName) {
        // Read ~/kc.json configuration file with user settings
        string configFile = "kc-" + env + ".json";
        var configuration = new ConfigurationBuilder()
          .SetBasePath(GetHomeFolder())
          .AddJsonFile(configFile, optional: false)
          .Build();
/*
        Console.WriteLine("-------------------------------------------------------------------------");
        Console.WriteLine("Config file:     " + configFile);
        Console.WriteLine("Host:            " + configuration.GetSection("Server")["bootstrap"]);
        Console.WriteLine("SSL CA location: " + configuration.GetSection("SSL")["SslCaLocation"]);
        Console.WriteLine("SSL certificate: " + configuration.GetSection("SSL")["SslCertificateLocation"]);
        Console.WriteLine("SSL key:         " + configuration.GetSection("SSL")["SslKeyLocation"]);
        //Console.WriteLine("SSL password:    " + configuration.GetSection("SSL")["SslKeyPassword"]);
        Console.WriteLine($"FOLLOWING TOPIC: {topicName}");

        // Inspect configuration object using a breakpoint here
        Console.WriteLine("-------------------------------------------------------------------------");
*/
        try {
            /* For reference, this is my client.properties file
             * 
            # In an SSL connection, a truststore is used to store certificates from 
            # Certified Authorities (CA) that verify the certificate presented by 
            # the server, while a keystore is used to store private key and identity 
            # certificates that a specific program should present to both parties 
            # (server or client) for verification. 
            #
            # In other words, the truststore is used to verify the credentials, 
            # while the keystore is used to provide those credentials.

            security.protocol=SSL

            #Public key
            # the keystore is used to provide the credentials
            ssl.keystore.location=user.p12
            ssl.keystore.password=VCPnBUxUHU6X
            ssl.keystore.type=PKCS12

            # Private key
            # the truststore is used to verify the credentials
            # Can also be saved as a .pem/.crt with no password
            ssl.truststore.location=ca.p12
            ssl.truststore.password=MZNhFgRH3KwG
             */
            // Configuration
            // Confluent documentation:
            // https://docs.confluent.io/platform/current/clients/confluent-kafka-dotnet/_site/api/Confluent.Kafka.ConsumerConfig.html
            var kafkaConfig = new ConsumerConfig {
                GroupId = "saf-group-application-accepted-decoded-04",
                BootstrapServers = configuration.GetSection("Server")["bootstrap"],
                SecurityProtocol = SecurityProtocol.Ssl,
                EnableAutoOffsetStore = false,
                EnableAutoCommit = true,
                AutoOffsetReset = AutoOffsetReset.Earliest,
                EnablePartitionEof = false,
                //Debug = "all",

                // CA certificates key (Path to CA certificate key, for verifying the broker's key)
                // oc --namespace=be5301-test get secret rsbc-ride-redhat-kafka-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt
                SslCaLocation = configuration.GetSection("SSL")["SslCaLocation"],

                // Public key file (Path to user certificate file)
                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.crt}' | base64 --decode > user.crt
                SslCertificateLocation = configuration.GetSection("SSL")["SslCertificateLocation"],

                // Private key file (Path to client's private key (PEM), used for authentication)
                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.key}' | base64 --decode > user.key
                SslKeyLocation = configuration.GetSection("SSL")["SslKeyLocation"],
                // Private key passphrase (for use with ssl.key.location and set_ssl_cert())

                // oc --namespace=be5301-test get secret kafkarideuser -o jsonpath='{.data.user\.password}' | base64 --decode
                SslKeyPassword = configuration.GetSection("SSL")["SslKeyPassword"],
            };

            using (var consumerBuilder = new ConsumerBuilder<Ignore, string>(kafkaConfig)
                .SetErrorHandler((_, e) => {
                    // ignore or log SSL errors and disconnection errors
                    /*if (e.Code != ErrorCode.Local_Ssl && e.Code != ErrorCode.Local_Transport) {
                        Console.WriteLine($"GENERIC ERROR: {e.Reason}");
                    }
                    else if (e.Code != ErrorCode.Local_Ssl) { Console.WriteLine($"LOCAL SSL ERROR:{e.Reason}"); }
                    else if (e.Code != ErrorCode.Local_Transport) { Console.WriteLine($"LOCAL TRANSPORT ERROR:{e.Reason}"); }
                    */
                })
                .Build()) {
                consumerBuilder.Subscribe(topicName);
                var cancelToken = new CancellationTokenSource();

                // Message consumption loop
                try {

                    // List of seen messages by offset. This ensures we only display messages once.
                    // The obvious downside is that memory will be consumed for each TopicPartitionOffset,
                    // but we don't expect to see millions of messages. Maybe tens or a few hundred, max.
                    List<Confluent.Kafka.TopicPartitionOffset> observedMessages = new List<Confluent.Kafka.TopicPartitionOffset>();
                    while (true) {

                        // This is a blocking method unless a time-out is given
                        var consumer = consumerBuilder.Consume(TimeSpan.FromSeconds(1));
                        //var record = JsonSerializer.Deserialize<String>(consumer.Message.Value);

                        if (consumer != null) {
                            var time = consumer.Timestamp;

                            if (!observedMessages.Contains(consumer.TopicPartitionOffset)) {
                                DateTime pacificTime = TimeZoneInfo.ConvertTimeFromUtc(consumer.Message.Timestamp.UtcDateTime, TimeZoneInfo.Local);
                                Console.Write(pacificTime.ToString("yyyy-MM-dd HH:mm:ss.fff zz "));
                                Console.WriteLine(consumer.Message.Value);
                                observedMessages.Add(consumer.TopicPartitionOffset);
                            }

                        }
/*
                        // Check if any key has been pressed
                        if (Console.KeyAvailable) {
                            // Read the last key pressed
                            var key = Console.ReadKey(true);

                            // Check if it is the Escape key
                            if (key.Key == ConsoleKey.Escape) {
                                // Break out of the loop
                                break;
                            }
                            else if (key.Key == ConsoleKey.Enter) {
                                Console.WriteLine();
                            }
                            else if (key.Key == ConsoleKey.M) {
                                // get current console character width
                                int terminalWidth = Console.BufferWidth;
                                if (terminalWidth > 0) {
                                    // Print a character across the width of the terminal
                                    for (int i = 0; i < terminalWidth; i++) {
                                        Console.Write("─");
                                    }
                                    Console.WriteLine();
                                }

                            }
                        }*/
                    }
                }
                catch (OperationCanceledException) {
                    Console.WriteLine("EXCEPTION READING MESSAGES: closing consumer...");
                    consumerBuilder.Close();
                }
            }
        }
        catch (Exception ex) {
            Console.WriteLine("\n\nException: " + ex.Message);
            System.Diagnostics.Debug.WriteLine(ex.Message);
        }
    }


    static string GetHomeFolder() {
        return Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
    }

    static string GetHelpPageText() {
        return @"Kafka consumer console app
==========================

This console app will list all the topics on a Kafka cluster, and allow you to subscribe
to messages in a topic. To set it up, you must create a configuration file in your home
folder named kc-<environment>.json, where <environment> is the OpenShift environment to 
use (dev, test, or prod).


Examples of usage:

    kc

        Show usage information.

    kc list [--env <dev|test|prod]

        Show a list of topics on the cluster.

    kc tail rsbc.apr.application.accepted.decoded [--env <dev|test|prod]

        Print all messages in a topic.


Examples of usage when redirecting STDOUT and STDERR:

    kc tail rsbc.apr.application.accepted.decoded --env test 2>$null

        Suppress STDERR output from the Kafka library.

    kc tail rsbc.apr.application.accepted.decoded --env test 2> $null | Tee-Object -FilePath stdout.log

        Suppress STDERR and send STDOUT to a file and the console.

    kc tail rsbc.apr.application.accepted.decoded 2> $null | jq --color-output .

        Use jq to colourise the output.

    kc tail rsbc.apr.application.accepted.decoded 2> $null | jq --color-output -c .

        Use jq to colourise the output, but keep records condensed on one line.

Interactions when consuming topics
    
When the consumer is printing messages, you can press the Enter key to insert an empty line. Press the M
key to insert a horizontal line marker. This is helpful to create a visual break or marker when monitoring
the logs manually. Press Esc or ^C to exit the consumer.
";
    }
}