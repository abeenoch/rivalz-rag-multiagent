import { HardhatRuntimeEnvironment } from 'hardhat/types'

module.exports = async ({ getNamedAccounts, deployments }: HardhatRuntimeEnvironment) => {
  const { deploy } = deployments
  const { deployer } = await getNamedAccounts()

  const coordinatorAddress = process.env.COORDINATOR_ADDRESS
  const ADCSConsumerName = `ADCSConsumer_v0.1`

  const ADCSConsumerDeployment = await deploy(ADCSConsumerName, {
    contract: 'MockADCSConsumer',
    args: [coordinatorAddress],
    from: deployer,
    log: true
  })

  console.log('MockADCSConsumer deployed at', ADCSConsumerDeployment.address)
}
